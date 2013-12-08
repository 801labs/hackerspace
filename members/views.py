# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from members.forms import *
from members.models import *
from datetime import datetime  
from django.shortcuts import redirect
from django.conf import settings
import braintree
import time


client_side_key = settings.BRAINTREE_CLIENT_KEY

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def index(request):

    if request.user.is_authenticated():
        if request.user.member_level.level >= 50:
            page_data = {'user':request.user}
            variables = RequestContext(request, page_data)
            return render_to_response('members/index.html', variables)
        else:
            page_data = {
                    'user':request.user,
                    'message':'Thank you for registering your account needs to be approved before you can do anything.'
                    }
            variables = RequestContext(request,page_data)
            return render_to_response('members/index.html', variables)

    return render_to_response('members/index.html', RequestContext(request))


def create_customer(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        pass
    """        braintree_model = BrainTreeModel()

        customer = { 'first_name'  : request.POST['first_name'],
                     'last_name'   : request.POST['last_name'],
                     'postal_code' : request.POST['postal_code'],
                     'account'     : request.POST['account'],
                     'month' : request.POST['month'],
                     'year' : request.POST['year'],
                     'cvv'              : request.POST['cvv'],
                    }

        if braintree_model.create_customer(customer):
            message = 'Transaction Succesful'
            variables = RequestContext(	request, {'message':message,
					          'client_side_key':client_side_key,})
            return render_to_response('payment/customer.html', RequestContext(request,variables))
        else:
            message = 'Transaction Failed'
            variables = RequestContext(	request, {'message':message,
					          'client_side_key':client_side_key,})
            return render_to_response('payment/customer.html', RequestContext(request,variables))

    variables = RequestContext(request, {'client_side_key':client_side_key})
    return render_to_response('payment/customer.html', RequestContext(request,variables))
    """


def payment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.user.member_level.level >= 50:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        
        account  = ''
        cvv      = ''
        month    = ''
        year     = ''
        amount   = ''

        braintree_model = BrainTree()
        data = request.POST

        error = False 
        error_message = ''
        if 'number' in data:
            pass
        else:
            error = True
            error_message = error_message + 'Account Number is Required. ' 
        if 'cvv' in data:
            pass
        else:
            error = True
            error_message = error_message + 'CVV is Required. '

        if 'payment_level' in data:
            pattern = r'^[1-4]{1}$'
            result = re.match(pattern, data['payment_level'].strip())
            print data['payment_level']
            if result:
                if data['payment_level'] == '1':
                    amount = '50.00'
                elif data['payment_level'] == '2':
                    amount = '75.00'
                elif data['payment_level'] == '3':
                    amount = '100.00'
                elif data['payment_level'] == '4':
                    amount = '200.00'
                else:
                    error = True
                    error_message = error_message + ' Payment Level is invalid. '
            else:
                error = True
                error_message = error_message + ' Amount is Invalid. ' 
        
        else:
            error = True
            error_message = error_message + ' Amount is Required. ' 
        if 'year' in data:
            pattern = r'^[0-9]{4}$'
            result = re.match(pattern, data['year'].strip())
            if result:
                pass
            else:
                error = True
                error_message = error_message + 'Year is Invalid. ' 
        else:
            error = True
            error_message = error_message + 'Year is Required. ' 
        if 'month' in data:
            pattern = r'^[0-9]{2}$'
            result = re.match(pattern, data['month'].strip())
            if result: 
                pass
            else:
                error = True
                error_message = error_message + 'Month is Invalid. '
        else:
            error = True
            error_message = error_message + 'Month is Required. ' 

        if error:
            variables = RequestContext(request, {'message':error_message,'client_side_key':client_side_key})
            return render_to_response('payment/singlepayment.html', variables)
   

        account  = request.POST['number'].strip()
        cvv      = request.POST['cvv'].strip()
        month    = request.POST['month'].strip()
        year     = request.POST['year'].strip()

        payment     = { 'account'   :account,
                        'cvv'       :cvv,
                        'month'     :month,
                        'year'      :year,
                        'amount'    :amount,
                        }
        
        transaction = braintree_model.create_transaction(payment,request.user)

        if transaction.success:
            message = 'Transaction Succesful'
            variables = RequestContext(request, {'message':message,'amount':payment['amount'],'transaction_id':transaction.id})
            return render_to_response('payment/singlepaymentsuccessful.html', variables)

        else:
            message = 'Sorry your transaction FAILED please try again'
            variables = RequestContext(request, {'message':message,'client_side_key':client_side_key})
            return render_to_response('payment/singlepayment.html', variables)

    variables = RequestContext(request,{'client_side_key':client_side_key})
    return render_to_response('payment/singlepayment.html', variables)

def login(request):


    if request.user.is_authenticated():
        return render_to_response('members/index.html', RequestContext(request))

    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if not form.is_valid():
            message = "Registration failed please try again."
            form = LoginForm()
            variables = RequestContext(request, {'form': form,'message':message})
            return render_to_response('registration/login.html',variables)


        u_email     = request.POST['email']
        u_password  = request.POST['password']

        if validateEmail(u_email):
            try:
                user = DC801User.objects.get(email=u_email)
            except DC801User.DoesNotExist:
                 message = "Your username or password is incorrect."
                 form = LoginForm()
                 variables = RequestContext(request, {'form': form,'message':message})
                 return render_to_response('registration/login.html',variables)
        else:
            message = "Your username or password is incorrect."
            form = LoginForm()
            variables = RequestContext(request, {'form': form,'message':message})
            return render_to_response('registration/login.html',variables)

        if user.is_active:
            user = authenticate(username=u_email, password=u_password)
            if user is not None:
                if user.check_password(u_password):
                     auth_login(request,user)
                     return redirect('/')
                else:
                     message = "Your username or password is incorrect."
                     form = LoginForm()
                     variables = RequestContext(request, {'form': form,'message':message})
                     return render_to_response('registration/login.html',variables)
            else:
                message = "Your username or password is incorrect."
                form = LoginForm()
                variables = RequestContext(request, {'form': form,'message':message})
                return render_to_response('registration/login.html',variables)


        

    else:
        form = LoginForm()
        variables = RequestContext(request, {'form': form})
        return render_to_response('registration/login.html',variables)


def register_success(request):
    return render_to_response('registration/register_success.html', RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):

    if request.user.is_authenticated():
      return render_to_response('members/index.html', RequestContext(request))

    if request.method == 'POST':
      form = RegistrationForm(request.POST)

      if form.is_valid():
        user = DC801User.objects.create_user(
                  email         =    form.cleaned_data['email'],
                  password      =    form.cleaned_data['password1'],
                  handle        =    form.cleaned_data['handle'],
                  first_name    =    form.cleaned_data['first_name'],
                  last_name     =    form.cleaned_data['last_name'],
                  phone_number  =    form.cleaned_data['phone_number'],
        )
        return HttpResponseRedirect('/register/success/')

    else:
      form = RegistrationForm()

    variables = RequestContext(request, {
      'form': form
    })
    return render_to_response('registration/register.html', variables)


