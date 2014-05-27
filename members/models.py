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
        except Exception,ex:
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
    
    date_joined       = models.DateTimeField(_('date joined'), default=timezone.now)
    objects           = DC801UserManager()
    first_name        = models.CharField(max_length=254, blank=True)
    last_name         = models.CharField(max_length=254, blank=True)
    member_level      = models.ForeignKey('MemberLevel',default=1)
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


class Transaction(models.Model):

    id              = models.AutoField(primary_key=True)
    user            = models.ForeignKey(DC801User)
    amount          = models.DecimalField( max_digits=19,decimal_places=2)
    payment_date    = models.DateTimeField(_('payment_date'), default=timezone.now)
    timestamp       = models.PositiveIntegerField()
    success         = models.BooleanField()

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

    braintree.Configuration.configure(braintree_environment,
                                    merchant_id   = merchant_id,
                                    public_key    = public_key,
                                    private_key   = private_key)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'nothing here'

    def delete_card(self,token):

        try:
            delete_response = braintree.CreditCard.delete(token)
            return delete_response
        except Exception,ex:
            f = open('/tmp/deletecard','w')
            f.write(repr(ex))
            f.close()
            return None




    def get_subscription(self,subscription_id):

        try:
            subscription = braintree.Subscription.find(subscription_id)
            return subscription
        except Exception,ex:
            f = open('/tmp/subscription_errors','w')
            f.write(repr(ex))
            f.close()
            return None


    def cancel_subscription(self,subscription_id):

        try:
            result = braintree.Subscription.cancel(subscription_id)
            return result
        except:
            f = open('/tmp/subscription_errors','w')
            f.write(repr(ex))
            f.close()
            return None




    def create_transaction(self,payment,user):
        #user = DC801User.objects.get(id=user.id)
        now = timezone.now()
        result = None
        try:
            result = braintree.Transaction.sale({

                "amount"                : payment['amount'],
                "credit_card": {
                    "number"            : payment['account'],
                    "cvv"               : payment["cvv"],
                    "expiration_month"  : payment["month"],
                    "expiration_year"   : payment["year"]

                },
                "customer":{
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,
                },
                "options": {
                    "submit_for_settlement": True,
                }
            })

            if result.is_success:
                transaction = Transaction(user = user,
                                                amount=payment['amount'],
                                                payment_date=now,
                                                timestamp=time.time(),
                                                success=1,
                                                )
                transaction.save()
                return transaction
            else:
                transaction = Transaction(user = user,
                                                amount=payment['amount'],
                                                payment_date=now,
                                                timestamp=time.time(),
                                                success=0
                                                )
                transaction.save()
                return transaction
        except Exception,ex:
            f = open('/tmp/payment_errors','w')
            f.write(repr(ex))
            f.close()

    def get_braintree_customer(self,customer_id):

        try:
            customer = braintree.Customer.find(customer_id)
            return customer
        except braintree.exceptions.NotFoundError:
            return None

    def addcard_to_customer(self,addcard):
        try:

            addcard_request = {
                        "customer_id"       : addcard['customer_id'],
                        "number"            : addcard['account'],
                        "expiration_month"  : addcard["month"],
                        "expiration_year"   : addcard["year"],
                        "cvv"               : addcard["cvv"],
                        "cardholder_name"   : addcard['first_name'] + " " + addcard['last_name'],
                    }

            f = open('/tmp/addcard_request','a')
            f.write(repr(addcard_request))
            f.close()
          


            result = braintree.CreditCard.create(addcard_request) 

            f = open('/tmp/addcard_result','a')
            f.write(repr(result))
            f.close()
          

            return result
        except braintree.exceptions.NotFoundError:
            return None

    def set_subscriptions(self,card_token,plan_id):

        try:
            result = braintree.Subscription.create({
                "payment_method_token": card_token,
                "plan_id": plan_id
            })
            return result
        except braintree.exceptions.NotFoundError:
            return None


    def create_customer(self,customer):

        result = braintree.Customer.create({
            "id": customer['id'],
            "first_name"    : customer["first_name"],
            "last_name"     : customer["last_name"],
            "email"         : customer["email"],
            "credit_card"   : {
                "billing_address"   : {
                                "postal_code"   : customer["postal_code"]
                                    },
                "number"            : customer["account"],
                "expiration_month"  : customer["month"],
                "expiration_year"   : customer["year"],
                "cvv"               : customer["cvv"]
            }
        })

        if result.is_success:
            return result
        else:
            return None
