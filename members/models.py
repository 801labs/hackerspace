from django.db import models
import braintree
import time
import random
import string
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,UserManager)
from django.core.mail import send_mail
from django.core import validators
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class DC801UserManager(BaseUserManager):

    def _create_user(self, email,handle, password,is_superuser,first_name,last_name,phone_number):
        """
        Creates and saves a User with the given email and password.
        """

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))

        email = self.normalize_email(email)
        user = self.model(email=email,
                        handle=handle,
                        is_active=True,
                        is_superuser=is_superuser, 
                        last_login=now,
                        date_joined=now,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        confirmation_code=confirmation_code,
                        )
        user.set_password(password)
        user.save(using=self._db)
        self.send_registration_confirmation(handle,email,confirmation_code)
        return user

    def create_user(self, email, handle, password=None, first_name=None, last_name=None, phone_number=None):
        return self._create_user(email,handle,password, False,first_name,last_name,phone_number)

    def create_superuser(self, email, handle, password, first_name=None, last_name=None, phone_number=None):
        return self._create_user(email,handle, password, True, first_name, last_name,phone_number)

    def send_registration_confirmation(self,handle,email,confirmation_code):

        title = "801 labs account confirmation"
        content = "http://www.801labs.org/confirm/" + str(confirmation_code) + "/" + handle
        try:
            pass
            #send_mail(title, content, 'no-reply@801labs.org', [email], fail_silently=False)
        except Exception as ex:
            f = open('/tmp/sendmail','w')
            f.write(repr(ex))
            f.close()

class MemberLevel(models.Model):

    id          = models.AutoField(primary_key=True)
    level       = models.PositiveIntegerField(unique=True)
    name        = models.CharField(max_length=254)
    description = models.CharField(max_length=254)

    def __unicode__(self):  # Python 3: def __str__(self):
        return 'Level: ' + str(self.level) +' ' +str(self.name)

class DC801User(AbstractBaseUser,PermissionsMixin):

    id               = models.AutoField(primary_key=True)
    email            = models.CharField(max_length=254, unique=True, db_index=True)
    handle           = models.CharField(max_length=254, unique=True)
    is_active        = models.BooleanField(_('active'), default=True,
                                            help_text=_('Designates whether this user should be treated as '
                                             'active. Unselect this instead of deleting accounts.'))
    is_member         = models.BooleanField(_('active'), default=True,
                                                          help_text=_('Designates whether this user is a paying member '
                                                                'active. Unselect this instead of deleting accounts.'))
    confirmed_email   = models.BooleanField(_('confirmed'), default=True,
                                                          help_text=_('Designates whether this user confirmed there email '
                                                                'confirmed.'))



    date_joined       = models.DateTimeField(_('date joined'), default=timezone.now)
    objects           = DC801UserManager()
    first_name        = models.CharField(max_length=254, blank=True)
    last_name         = models.CharField(max_length=254, blank=True)
    member_level      = models.ForeignKey('MemberLevel',default=1,on_delete=models.CASCADE)
    phone_number      = models.CharField(max_length=11, blank=True)
    confirmation_code = models.CharField(max_length=33, blank=True)
    subscription_code = models.CharField(max_length=254, blank=True)

    USERNAME_FIELD   = 'email'
    REQUIRED_FIELDS = ['handle','first_name','last_name','phone_number']


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):  # Python 3: def __str__(self):
        return  str(self.handle)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


    def reset_password(self):
        resetpassword = ResetPasswordCode(  user=self,
                                            timestamp=time.time(),
                                            used=False,
                                          )

        reset_code = resetpassword.create_confirmation_code()
        resetpassword.confirmation_code = reset_code
        resetpassword.save()

        title = "801 Labs password reset."
        content = "Click Here to reset your password - http://www.801labs.org/reset/" + str(reset_code)

        try:
            send_mail(title, content, 'no-reply@801labs.org', [self.email], fail_silently=False)
        except Exception as ex:
            f = open('/tmp/sendmail','w')
            f.write(repr(ex))
            f.close()

        

class ResetPasswordCode(models.Model):

    id                  = models.AutoField(primary_key=True)
    user                = models.ForeignKey(DC801User,on_delete=models.CASCADE)
    timestamp           = models.PositiveIntegerField()
    used                = models.BooleanField(default=False)
    confirmation_code   = models.CharField(max_length=33, blank=True)

    def create_confirmation_code(self):
        confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
        return confirmation_code


class Transaction(models.Model):

    id              = models.AutoField(primary_key=True)
    user            = models.ForeignKey(DC801User,on_delete=models.CASCADE)
    amount          = models.DecimalField( max_digits=19,decimal_places=2)
    payment_date    = models.DateTimeField(_('payment_date'), default=timezone.now)
    timestamp       = models.PositiveIntegerField()
    success         = models.BooleanField()
    transaction_id  = models.TextField(null=True)
    status          = models.TextField(null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return 'ID: ' +str(self.id) + ' User: '+ str(self.user.first_name) +' '+str(self.user.last_name) + ' Success: ' + str(self.success)  + ' Amount: '+ str(self.amount)


class BrainTree(models.Model):

    merchant_id = settings.BRAINTREE_MERCHANT_ID
    public_key  = settings.BRAINTREE_PUBLIC_KEY
    private_key = settings.BRAINTREE_PRIVATE_KEY
    braintree_environment = None

    if settings.BRAINTREE_ENVIRONMENT == 'sandbox':
        braintree_environment = braintree.Environment.Sandbox

    if settings.BRAINTREE_ENVIRONMENT == 'production':
        braintree_environment = braintree.Environment.Production

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree_environment,
            merchant_id   = merchant_id,
            public_key    = public_key,
            private_key   = private_key
        )
    )
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'nothing here'

    def generate_client_token(self, customer=None):
        client_data = {}

        if customer:
            client_data = {
                "customer_id": customer.id,
            }

        return self.gateway.client_token.generate(client_data)

    def transact(self, options):
        return self.gateway.transaction.sale(options)

    def find_transaction(self, id):
        return self.gateway.transaction.find(id)

    def delete_card(self,token):

        try:
            delete_response = self.gateway.credit_card.delete(token)
            return delete_response
        except Exception as ex:
            f = open('/tmp/deletecard','w')
            f.write(repr(ex))
            f.close()
            return None




    def get_subscription(self,subscription_id):

        try:
            subscription = self.gateway.subscription.find(subscription_id)
            return subscription
        except Exception as ex:
            f = open('/tmp/subscription_errors','w')
            f.write(repr(ex))
            f.close()
            return None


    def cancel_subscription(self,subscription_id):

        try:
            result = self.gateway.subscription.cancel(subscription_id)
            return result
        except Exception as ex:
            f = open('/tmp/subscription_errors','w')
            f.write(repr(ex))
            f.close()
            return None




    def create_transaction(self,payment,user):
        #user = DC801User.objects.get(id=user.id)
        now = timezone.now()
        result = None
        try:
            result = self.gateway.transaction.sale({

                "amount": payment['amount'],
                "payment_method_nonce": payment['nonce'],
                "customer":{
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,
                },
                "options": {
                    "submit_for_settlement": True,
                }
            })
            
            success = 0

            if result.is_success:
                success = 1

            transaction = Transaction(
                transaction_id = result.transaction.id,
                user = user,
                amount=payment['amount'],
                payment_date=now,
                timestamp=time.time(),
                success=success,
                status = result.transaction.status,
            )
            transaction.save()
            return result
        except Exception as ex:
            f = open('/tmp/payment_errors','w')
            f.write(repr(ex))
            f.close()

    def get_braintree_customer(self,customer_id):

        try:
            customer = self.gateway.customer.find(str(customer_id))
            return customer
        except braintree.exceptions.NotFoundError:
            return None

    def get_plans(self):
        try:
            result = self.gateway.plan.all()
            return result
        except braintree.exceptions.NotFoundError:
            return None

    def get_transactions(self, customer_id):
        try:
            result = self.gateway.transaction.search(
                braintree.TransactionSearch.customer_id == str(customer_id)
            )
            return result
        except braintree.exceptions.NotFoundError:
            return None

    def get_payment_method(self, payment_method_token):
        try:
            result = self.gateway.payment_method.find(payment_method_token)
            return result
        except braintree.exceptions.NotFoundError:
            return None

    def get_subscriptions(self, customer_id):
        try:
            result = self.gateway.subscription.search(
                braintree.SubscriptionSearch.customer_id == str(customer_id)
            )
            return result
        except braintree.exceptions.NotFoundError:
            return None

    def set_subscription(self,customer,payment_method_nonce,plan_id,subscription=None):

        try:
            # if plan changes, we need to clear out the old plan and add a new plan
            if subscription and plan_id != subscription.plan_id:
                cancel_result = self.cancel_subscription(subscription.id)

                if cancel_result.is_success or cancel_result.message == 'Subscription has already been canceled.':
                    subscription = None
                else:
                    raise Exception("Unable to update subscription")
            
            # create new subscription if there isn't one, or the one on file has been canceled (if payment method is removed, subscription will be canceled)
            if subscription is None or subscription.status == 'Canceled':
                result = self.gateway.subscription.create({
                    # "payment_method_token": token_result.payment_method.token,
                    "payment_method_nonce": payment_method_nonce,
                    "plan_id": plan_id,
                })
            else:
                result = self.gateway.subscription.update(subscription.id, {
                    "payment_method_nonce": payment_method_nonce,
                })
            
            return result
        except braintree.exceptions.NotFoundError:
            pass

        return None

    def create_customer(self, user, payment_method_nonce=None):

        customer_data = {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,   
        }

        # associate a payment method with customer
        if payment_method_nonce:
            customer_data["payment_method_nonce"] = payment_method_nonce

        return self.gateway.customer.create(customer_data)

    def create_payment_method(self, user, payment_method_nonce):

        data = {
            "customer_id": str(user.id),
            "payment_method_nonce": payment_method_nonce,
        }

        return self.gateway.payment_method.create(data)

    def set_default_payment_method(self, token):

        data = {
            "options": {
                "make_default": True
            }
        }

        return self.gateway.payment_method.update(token, data)
