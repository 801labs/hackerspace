import re
from django import forms as forms
from django.contrib.auth.models import User
#from captcha.fields import ReCaptchaField    
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from members.models import DC801User
from django.contrib.admin.widgets import AdminDateWidget  #added by metacortex

textInputAttrs = {'size':'35', 'class':'form-control'}

class RegistrationForm(forms.Form):
    
    handle  = forms.CharField(label='Handle',widget=forms.TextInput(attrs=textInputAttrs), max_length=40)

    password1 = forms.CharField(
      label='Password',
      widget=forms.PasswordInput(attrs=textInputAttrs)
      ,help_text = '<p>Password must contain at least one lower chracter, one uppercase character, at least one number, at least one special charater, and be longer than eight charaters.</p>'
    )
    password2 = forms.CharField(
      label='Password (Again)',
      widget=forms.PasswordInput(attrs=textInputAttrs)
    )

    email           = forms.EmailField(label='Email',widget=forms.TextInput(attrs=textInputAttrs), max_length=254)
    phone_number    = forms.CharField(label='Phone Number',widget=forms.TextInput(attrs=textInputAttrs),max_length=11,help_text = "<p>Please format the phone number as 1801NXXNXXX <br/>(remember to put the 1 before the area code)</p>")
    first_name      = forms.CharField(label='First Name',widget=forms.TextInput(attrs=textInputAttrs),max_length=254)
    last_name       = forms.CharField(label='Last Name',widget=forms.TextInput(attrs=textInputAttrs),max_length=254)
    
    #OPTIONS = (
    #        ("1", "TheTransistor: Orem"),
    #        ("2", "TheTransistor: SLC"),
    #        )

    #primary_hacker_space = forms.ChoiceField(widget=forms.RadioSelect,
    #                                         choices=OPTIONS)

    #emergency_contact_name      = forms.CharField(max_length='254',label='Emergency Contact Name')
    #emergency_contact_phone     = forms.CharField(max_length='11',label='Emergency Contact Phone Number')

    #additional_questions = forms.CharField(label='Additional Questions / Comments ', widget=forms.Textarea)

    #captcha = ReCaptchaField(attrs={'theme' : 'clean'})

    def clean_handle(self):

      handle = self.cleaned_data['handle']

      if not re.search(r'^\w+$', handle):
        raise forms.ValidationError('Handle can only contain alphanumeric characters and the underscore.')

      try:
        DC801User.objects.get(handle=handle)
      except:
        return handle

      raise forms.ValidationError('Handle is already taken.')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if not re.search(r'^[0-9]{11}$', phone_number):
            raise forms.ValidationError('Phone Number is in valid please use 18015551234 format.')
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not re.search(r'^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$', first_name):
            raise forms.ValidationError('First Name contains invalid characters.')
        return first_name
     

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.search(r'^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$', last_name):
            raise forms.ValidationError('Last Name contains invalid characters.')
        return last_name


    def clean_email(self):

        email = self.cleaned_data['email']

        try:
            validate_email( email )
        except ValidationError:
            raise forms.ValidationError('Email is invalid.')

        try:
            DC801User.objects.get(email=email)
        except:
            return email

        raise forms.ValidationError('email is already registred.')



    def clean_password2(self):
      if 'password1' in self.cleaned_data:
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 == password2:

            valid_password = True
            message = ''

            if len(password2) < 8:
                valid_password = False
                message += 'Password must be longer than 8 characters. '

            if not re.search(r'(?=.*[\d])',password2):
                valid_password = False
                message += 'Password did not contain one number. '

            if not re.search(r'(?=.*[a-z])',password2):
                valid_password = False
                message += 'Password did not contain a lower case character. '

            if not re.search(r'(?=.*[A-Z])',password2):
                valid_password = False
                message += 'Password did not contain a capital character. '

            if not re.search(r'(?=.*[\!\@\#\$\%\&\*\(\)\^\[\]\;\:\'\-\_\+\=\{\}\[\]\?\<\>\ \.\,\|\`\\\/]+.*)',password2):
                valid_password = False
                message += 'Password did not contain a special character. '

            if valid_password:
                return password2
            else:
                raise forms.ValidationError(message)

      raise forms.ValidationError('Passwords do not match.')


class ResetForm(forms.Form):
    email = forms.CharField(label='Email',widget=forms.TextInput(attrs=textInputAttrs),max_length=254)

class ResetPasswordForm(forms.Form):
    
    reset_code = forms.CharField(required=False, max_length=50,widget=forms.HiddenInput())

    new_password1 = forms.CharField(
      label='Password',
      widget=forms.PasswordInput(attrs=textInputAttrs)
      ,help_text = '<br/><p>Password must contain at least one lower chracter, </br>one uppercase character, at least one number, at least one special charater,</br> and be longer than eight charaters.</p>'
    )

    new_password2 = forms.CharField(
      label='Password (Again)',
      widget=forms.PasswordInput(attrs=textInputAttrs)
    )

    def clean_new_password2(self):

        if 'new_password1' in self.cleaned_data:

            password1 = self.cleaned_data['new_password1']
            password2 = self.cleaned_data['new_password2']
        
            if password1 == password2:

                valid_password = True
                message = ''

                if len(password2) < 8:
                    valid_password = False
                    message += 'Password must be longer than 8 characters. '

                if not re.search(r'(?=.*[\d])',password2):
                    valid_password = False
                    message += 'Password did not contain one number. '

                if not re.search(r'(?=.*[a-z])',password2):
                    valid_password = False
                    message += 'Password did not contain a lower case character. '

                if not re.search(r'(?=.*[A-Z])',password2):
                    valid_password = False
                    message += 'Password did not contain a capital character. '

                if not re.search(r'(?=.*[\!\@\#\$\%\&\*\(\)\^\[\]\;\:\'\-\_\+\=\{\}\[\]\?\<\>\ \.\,\|\`\\\/]+.*)',password2):
                    valid_password = False
                    message += 'Password did not contain a special character. '

                if valid_password:
                    return password2
                else:
                    raise forms.ValidationError(message)

        raise forms.ValidationError('Passwords do not match.')


    

class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs=textInputAttrs),
        max_length=254
    )

    password = forms.CharField(
          label='Password',
          widget=forms.PasswordInput(attrs=textInputAttrs),
          max_length=254
    )

class DC801UserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(DC801UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = DC801User
        fields = ("email","handle")

class DC801UserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(DC801UserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = DC801User
        fields = '__all__'

#metacortex prform below

class PRForm(forms.Form):

    handle      = forms.CharField(label='Handle',widget=forms.TextInput(attrs=textInputAttrs),max_length=254)
    date        = forms.CharField(label='Date',widget = AdminDateWidget)
    time        = forms.CharField(label='Time',widget=forms.TextInput(attrs=textInputAttrs),max_length=7)
    reoccuring  = forms.BooleanField(label='Reoccuring',required=False)
    event       = forms.CharField(label='Event', widget=forms.TextInput(attrs=textInputAttrs),max_length=256)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows':'5'}), max_length=5000)
    notes       = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'rows':'3'}), max_length=5000,required=False)

    def clean_handle(self):
        handle = self.cleaned_data['handle'].strip()
        return handle

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        return description
     
    def clean_notes(self):
        notes = self.cleaned_data['notes'].strip()


        return notes

    def clean_event(self):
        event = self.cleaned_data['event'].strip()
        return event

"""   def clean_date(self):
        date = self.cleaned_data['date']
        print date 
        if not re.search(r'^\w+$', date):
            raise forms.ValidationError('Date is invalid.')
        return date
    def clean_time(self):
        time = self.cleaned_data['time']
        if not re.search(r'^\w+$', time):
            raise forms.ValidationError('Time is invalid.')
        return time
"""
