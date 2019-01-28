# Create your views here./
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
# from django.conf.urls.defaults import *
from django.core.exceptions import *
from members.forms import *
from members.models import *
from datetime import datetime  
from django.shortcuts import redirect
from django.conf import settings
import braintree
import time
import datetime

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def render_subscription(request,messages):

    braintree_customer              = None 
    braintree_plans                 = None
    braintree_customer_subscription = None
    braintree_payment_method        = None
    customer_cards                  = None

    braintree_model = BrainTree()
    braintree_customer = braintree_model.get_braintree_customer(request.user.id)
    client_token = braintree_model.generate_client_token(braintree_customer)

    try:
        braintree_plans     = braintree_model.get_plans()
    except Exception as ex:
        f = open('/tmp/braintree_getcustomer','a')
        f.write(repr(ex))
        f.close()

    if request.user.subscription_code is not None and request.user.subscription_code != '' and hasattr(request.user, 'subscription_code'):
        braintree_customer_subscription = braintree_model.get_subscription(request.user.subscription_code)

        if braintree_customer_subscription:
            braintree_payment_method = braintree_model.get_payment_method(braintree_customer_subscription.payment_method_token)

    page_data = {
        'subscription'      : braintree_customer_subscription,
        'payment_method'    : braintree_payment_method,
        'info_messages'     : messages['info_messages'],
        'success_messages'  : messages['success_messages'],
        'error_messages'    : messages['error_messages'],
        'client_token'      : client_token,
        'plans'             : braintree_plans,
        'customer'          : braintree_customer,
        'cards'             : customer_cards,
    }

    return render(request, 'payment/recurring_billing.html', page_data)

def payment_methods(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    error = False
    messages = {'error_messages':[]}
    braintree_model = BrainTree()

    card_token = None
    payment_method_nonce = None

    if request.method == 'POST' and 'action' in request.POST:
        braintree_customer = braintree_model.get_braintree_customer(request.user.id)

        action = request.POST['action']

        if action in ['default', 'remove']:
            if 'card' not in request.POST or len(request.POST['card']) < 1:
                error_message = "Invalid card specified"
                messages['error_messages'].append(error_message)
                error = True
            else:
                card_token = request.POST['card']
        elif action != 'add':
            error_message = "Invalid action specified"
            messages['error_messages'].append(error_message)
            error = True
        elif 'payment_method_nonce' not in request.POST or len(request.POST['payment_method_nonce']) < 1:
            error_message = "Invalid payment method"
            messages['error_messages'].append(error_message)
            error = True
        else:
            payment_method_nonce = request.POST['payment_method_nonce']

        if error:
            return render_payment_methods(request, messages)

        if action == 'default':
            result = braintree_model.set_default_payment_method(card_token)
        elif action == 'remove':
            result = braintree_model.delete_card(card_token)

            if 'remove_user_subscription' in request.POST:
                user_subscription_id = request.POST['remove_user_subscription']

                if user_subscription_id == request.user.subscription_code:
                    request.user.subscription_code = ''
                    request.user.save()
        elif action == 'add':
            if braintree_customer:
                result = braintree_model.create_payment_method(braintree_customer, payment_method_nonce)
            else:
                result = braintree_model.create_customer(request.user, payment_method_nonce)

        if result.is_success:
            return redirect('/payment/methods')
    
    return render_payment_methods(request)

def render_payment_methods(request, messages=None):
    braintree_model = BrainTree()

    braintree_customer = braintree_model.get_braintree_customer(request.user.id)
    client_token = braintree_model.generate_client_token()
    customer_cards = None

    if braintree_customer is not None and hasattr(braintree_customer, 'credit_cards'):
        customer_cards = braintree_customer.credit_cards

    page_data = {
        'client_token': client_token,
        'cards': customer_cards,
        'messages': messages,
        'user': request.user,
    }

    return render(request, 'payment/methods.html', page_data)


def payment_history(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    braintree_model = BrainTree()
    braintree_transactions = braintree_model.get_transactions(request.user.id)

    page_data = {
        'transactions'      : braintree_transactions.items,
    }

    return render(request, 'payment/history.html', page_data)

def index(request):

    if request.user.is_authenticated:
        request.session.modified = True
        if request.user.member_level.level >= 50:
            page_data = {'user':request.user}
            return render(request, 'members/index.html', page_data)
        else:
            page_data = {
                    'user':request.user,
                    'message':'Please come down to one of our meetings and hangout in irc http://webchat.freenode.net/ #dc801 chat.freenode.net or www.dc801.org. On Freenode #dc801 ask for Nemus, L34n or Metacortex for more information.'
                    }
            return render(request, 'members/index.html', page_data)

    return render(request, 'members/index.html')

def member_info(request):

    page_data = {'user':request.user}
    return render(request, 'members/member_info.html', page_data)

def contact_us(request):

    page_data = {'user':request.user}
    return render(request, 'members/contact_us.html', page_data)

def terms(request):

    page_data = {'user':request.user}
    return render(request, 'members/terms.html', page_data)





def faq(request):

    page_data = {'user':request.user}
    return render(request, 'members/faq.html', page_data)

def user_groups(request):

    page_data = {'user':request.user}
    return render(request, 'members/user_groups.html', page_data)

def gallery(request):

   page_data = {'user':request.user}
   return render(request, 'members/gallery.html', page_data)


def classes(request):

   page_data = {'user':request.user}
   return render(request, 'members/classes.html', page_data)


def blog(request):

   page_data = {'user':request.user}
   return render(request, 'members/blog.html', page_data)





def events(request):

   page_data = {'user':request.user}
   return render(request, 'members/events.html', page_data)


def subscriptions(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    request.session.modified = True
    braintree_model = BrainTree()
    braintree_customer = braintree_model.get_braintree_customer(request.user.id)

    messages = {}
    messages['info_messages']       = []
    messages['error_messages']      = []
    messages['success_messages']    = []

    braintree_customer_subscription = None

    message = ''

    if request.method == 'POST':
        if request.POST['method'] == 'cancel':

            #get subscription
            if request.user.subscription_code is not None and request.user.subscription_code != '' and hasattr(request.user, 'subscription_code'):
                braintree_customer_subscription = braintree_model.get_subscription(request.user.subscription_code)

            if braintree_customer_subscription is not None:

                cancel_result = braintree_model.cancel_subscription(braintree_customer_subscription.id)
                
                if cancel_result.is_success or cancel_result == 'Subscription has already been canceled.':

                    info_message = "Old Subscription \""+braintree_customer_subscription.plan_id+"\" Canceled. "
                    messages['info_messages'].append(info_message)

                    request.user.subscription_code = ''
                    request.user.save()
                    braintree_customer_subscription = None

                    subject = '801 Labs User Canceled Subscription - ' + str(request.user.handle)
                    message = 'User canceled subscription ' + str(request.user.handle)
                    send_mail(subject, message, 'no-reply@801labs.org', ['info@dc801.org'])

                    return render_subscription(request,messages)

                else:
                    info_message =  "Old Subscription \""+braintree_customer_subscription.plan_id+"\" was NOT canceled please call (385) 313-0801 and leave a voicemail. "
                    messages['info_messages'].append(info_message)

                    return render_subscription(request,messages)
            else:
                info_message = "You do not have a Subcription to Cancel. "
                messages['info_messages'].append(info_message)

                return render_subscription(request,messages)
 

        if request.POST['method'] in ['subscribe', 'update']:

            subscribe_error = False

            if 'payment_method_nonce' not in request.POST or len(request.POST['payment_method_nonce']) < 1:
                    error_message = "Cannot create subscription invalid payment method."
                    messages['error_messages'].append(error_message)
                    subscribe_error = True
                    

            if 'plan_id' not in request.POST or len(request.POST['plan_id']) < 1:
                    error_message = "Cannot create subscriptions user card invalid plan_id."
                    messages['error_messages'].append(error_message)
                    subscribe_error = True
                

            if subscribe_error:
                    return render_subscription(request,messages)

            #get data
            payment_method_nonce = request.POST['payment_method_nonce'].strip()
            plan_id    = request.POST['plan_id'].strip()


            if request.user.subscription_code is not None and request.user.subscription_code != '' and hasattr(request.user, 'subscription_code'):
                braintree_customer_subscription = braintree_model.get_subscription(request.user.subscription_code)

            if request.POST['method'] == 'update' and braintree_customer_subscription is None:
               
                error_message = "Can't find subscription \""+braintree_customer_subscription.plan_id+"\" to update. "
                messages['error_messages'].append(error_message)
                return render_subscription(request,messages)

            elif request.POST['method'] == 'subscribe' and braintree_customer_subscription is not None:

                error_message = "Please cancel subscription \""+braintree_customer_subscription.plan_id+"\" before creating a new one. "
                messages['error_messages'].append(error_message)
                return render_subscription(request,messages)
 
            else:

                subscription_response = braintree_model.set_subscription(braintree_customer, payment_method_nonce, plan_id, braintree_customer_subscription)

                if subscription_response.is_success:
                    
                    request.user.subscription_code = subscription_response.subscription.id
                    request.user.save()

                    braintree_customer_subscription  = subscription_response.subscription

                    if request.POST['method'] == 'subscribe':
                        success_message     = message +  " Created Subscription \""+subscription_response.subscription.plan_id+"\" successfully"

                        subject = '801 Labs User New Subscription - ' + str(request.user.handle)
                        message = 'User Subscription ' + str(request.user.handle) + ' ' + str(braintree_customer_subscription.plan_id)
                    else:
                        success_message     = message +  " Changed subscription \""+subscription_response.subscription.plan_id+"\" successfully"

                        subject = '801 Labs User Updated Subscription - ' + str(request.user.handle)
                        message = 'User Subscription ' + str(request.user.handle) + ' ' + str(braintree_customer_subscription.plan_id)

                    messages['success_messages'].append(success_message)
                    send_mail(subject, message, 'no-reply@801labs.org', ['info@dc801.org'])

                    return render_subscription(request,messages)

                else:
                    error_message = 'Setting Subscription Failed'
                    messages['error_messages'].append(error_message)
                    return render_subscription(request,messages)

    return render_subscription(request,messages)


def payment(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    #if not request.user.member_level.level >= 50:
    #    return HttpResponseRedirect('/')

    braintree_model = BrainTree()
    customer = braintree_model.get_braintree_customer(request.user.id)
    client_token = braintree_model.generate_client_token(customer)

    request.session.modified = True
    if request.method == 'POST':
        
        payment_method_nonce = ''
        amount = ''

        data = request.POST

        error = False 
        error_message = ''
        if 'payment_method_nonce' in data:
            payment_method_nonce = data['payment_method_nonce']
        else:
            error = True
            error_message = error_message + 'A valid payment method is required. ' 

        if 'payment_level' in data:
            pattern = r'^[1-9]{1}$'
            result = re.match(pattern, data['payment_level'].strip())

            if result:
                if data['payment_level'] == '1':
                    amount = '50.00'
                elif data['payment_level'] == '2':
                    amount = '75.00'
                elif data['payment_level'] == '3':
                    amount = '100.00'
                elif data['payment_level'] == '4':
                    amount = '200.00'
                elif data['payment_level'] == '5':
                    amount = '25.00'
                elif data['payment_level'] == '6':
                    amount = '300.00'
                elif data['payment_level'] == '7':
                    amount = '600.00'
                elif data['payment_level'] == '8':
                    amount = '450.00'
                elif data['payment_level'] == '9':
                    amount = '900.00'
             
                else:
                    error = True
                    error_message = error_message + ' Invalid payment level. '
            else:
                error = True
                error_message = error_message + ' Amount is Invalid. ' 
        
        else:
            error = True
            error_message = error_message + ' Amount is Required. ' 
        
        if error:
            page_data = {
                'message':error_message,
                'client_token':client_token,
                'customer':customer,
            }

            return render(request, 'payment/singlepayment.html', page_data)
   
        payment = {
            'nonce': payment_method_nonce,
            'amount': amount,
        }
        
        transaction_result = braintree_model.create_transaction(payment,request.user)

        if transaction_result is not None and transaction_result.is_success:
            if customer is None:
                # create user and attach payment method used
                result = braintree_model.create_customer(request.user)

            message = 'Transaction Succesful'
            page_data = {
                'message':message,
                'amount':payment['amount'],
                'transaction_id':transaction_result.transaction.id,
            }

            return render(request, 'payment/singlepaymentsuccessful.html', page_data)

        else:
            message = None
            if transaction_result:
                message = 'Sorry your transaction FAILED please try again. '

                if hasattr(transaction_result, 'message'):
                    message = message + transaction_result.message

            page_data = {
                'message':message,
                'client_token':client_token,
                'customer':customer,
            }

            return render(request, 'payment/singlepayment.html', page_data)

    page_data = {
        'client_token':client_token,
        'customer':customer,
    }
    
    return render(request, 'payment/singlepayment.html', page_data)

def login(request):

    if request.user.is_authenticated:
        return render(request, 'members/index.html')

    if request.method == 'POST':
        request.session.modified = True    
        form = LoginForm(request.POST)
        if not form.is_valid():
            message = "Registration failed please try again."
            form = LoginForm()
            page_data = {'form': form,'message':message}
            return render(request, 'registration/login.html', page_data)


        u_email     = request.POST['email']
        u_password  = request.POST['password']

        if validateEmail(u_email):
            try:
                user = DC801User.objects.get(email=u_email)
            except DC801User.DoesNotExist:
                 message = "Your username or password is incorrect."
                 form = LoginForm()
                 page_data = {'form': form,'message':message}
                 return render(request, 'registration/login.html', page_data)
        else:
            message = "Your username or password is incorrect."
            form = LoginForm()
            page_data = {'form': form,'message':message}
            return render(request, 'registration/login.html', page_data)

        if user.is_active:
            user = authenticate(username=u_email, password=u_password)
            if user is not None:
                if user.check_password(u_password):
                     auth_login(request,user)
                     return redirect('/')
                else:
                     message = "Your username or password is incorrect."
                     form = LoginForm()
                     page_data = {'form': form,'message':message}
                     return render(request, 'registration/login.html', page_data)
            else:
                message = "Your username or password is incorrect."
                form = LoginForm()
                page_data = {'form': form,'message':message}
                return render(request, 'registration/login.html', page_data)

    else:
        request.session.modified = True
        form = LoginForm()
        page_data = {'form': form}
        return render(request, 'registration/login.html', page_data)


def register_success(request):
    return render(request, 'registration/register_success.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def reset_page(request):

    if request.user.is_authenticated:
      return render(request, 'members/index.html')

    if request.method == 'POST':
        
        form = ResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            form = ResetForm()

            try:
                user = DC801User.objects.filter(email=email)

                if not user:

                    page_data = { 'form': form, 'message':'Reset email sent to ' + str(email) }
                else:

                    page_data = { 'form': form, 'message':'Reset email sent to ' + str(email) }

                    user[0].reset_password()
     
            except ObjectDoesNotExist:
                    page_data = { 'form': form, 'message':'Failure' + str(email) }
              
                    user = None

            return render(request, 'registration/reset_email.html', page_data)

        else:
            form = ResetForm()

            page_data = { 'form': form }

            return render(request, 'registration/reset_email.html', page_data)

    else:
        form = ResetForm()

        page_data = { 'form': form }

        return render(request, 'registration/reset_email.html', page_data)

def reset_code(request,reset_code):

    if request.user.is_authenticated:
      return render(request, 'members/index.html')

    form = ResetPasswordForm(initial={'reset_code': reset_code})

    try:

        reset = ResetPasswordCode.objects.filter(confirmation_code=str(reset_code))
        
        if reset[0].used:
            return redirect('/')
        
        #reset time
        lapse_time = time.time() - 86400
        
        if reset[0].timestamp < lapse_time:
            return redirect('/')

        if request.method == 'POST':

            form = ResetPasswordForm(request.POST)

            if form.is_valid():

                reset_obj = ResetPasswordCode.objects.get(id=reset[0].id)
                new_password  = form.cleaned_data['new_password1']
                user = DC801User.objects.get(id=reset[0].user.id)
                user.set_password(new_password)
                user.save()
                reset_obj.used = True
                reset_obj.save()

                page_data = {
                    'message': 'Password succesful changed please login.'
                }

                return render(request, 'registration/reset_password_success.html', page_data)
            else:
                page_data = {
                    'form'      : form, 
                    'message'   : '' ,
                    'reset_code': reset_code
                }
    
                return render(request, 'registration/reset_password.html', page_data)
 
        if not reset:
            return redirect('/')
        else:

            page_data = {
                'form'      : form, 
                'message'   : 'Reset Password',
                'reset_code': reset_code
            }

            return render(request, 'registration/reset_password.html', page_data)
    
      
    except ObjectDoesNotExist:

        
        page_data = {
                        'form'      : form, 
                        'message'   :'Failure' + str(reset_code),
                        'reset_code': reset_code,
                    }
              
        return render(request, 'registration/reset_password.html', page_data)
    return redirect('/')



def register_page(request):

    if request.user.is_authenticated:
        return render(request, 'members/index.html')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = DC801User.objects.create_user(
                email        = form.cleaned_data['email'],
                password     = form.cleaned_data['password1'],
                handle       = form.cleaned_data['handle'],
                first_name   = form.cleaned_data['first_name'],
                last_name    = form.cleaned_data['last_name'],
                phone_number = form.cleaned_data['phone_number'],
            )
            return HttpResponseRedirect('/register/success/')

        else:
            page_data = { 'form': form }
            return render(request, 'registration/register.html', page_data)
    else:
        form = RegistrationForm()
        page_data = { 'form': form }
        return render(request, 'registration/register.html', page_data)

def pr_request(request):

    #if user is not authenticated then redirect them
    if not request.user.is_authenticated:
        return HttpResponse(status=404)

    if request.method == 'POST':

    
        PRform = PRForm(request.POST)
        if PRform.is_valid():

            emailsubject = str(request.user.handle) + " PR REQUEST " + str(datetime.datetime.now())
            # do something 
            #success message blah blah
            try:
                message = "\r 801 Handle: "   + str(request.user.handle) + "\r Form Handle: "  + str(PRform.cleaned_data['handle']) + "\r Date: "         + str(PRform.cleaned_data['date']) + "\r Time: "         + str(PRform.cleaned_data['time'])  + "\r Reoccuring: "   + str(PRform.cleaned_data['reoccuring']) + "\r Event:  "       + str(PRform.cleaned_data['event']) + "\r Description:  " + str(PRform.cleaned_data['description'].encode("ascii", "ignore")) + "\r Notes: "        + str(PRform.cleaned_data['notes'].encode("ascii", "ignore"));
                send_mail(emailsubject, 
                            message, 
                            'no-reply@801labs.org', 
                            ['board@801labs.org'])

                page_data = {
                    'message' : "Request Submited Successfully",
                    'form': PRform
                }

                return render(request, 'members/pr_request.html', page_data)

            except Exception as e:
                page_data = {
                    'message' : "Request Failed ",
                    'form': PRform
                }
                f = open('/tmp/pr_error','a')
                f.write(repr(e))
                f.close()

                return render(request, 'members/pr_request.html', page_data)
            

        else:
            #error message
            page_data = {
                'message': 'Submition failed',
                'form': PRform
            }
            return render(request, 'members/pr_request.html', page_data)

    page_data = {
        'form': PRForm
    }
    return render(request, 'members/pr_request.html', page_data)
