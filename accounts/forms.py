from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django.contrib.auth import (
authenticate,
get_user_model,
logout,
	)
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect


class UserLoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'username','placeholder':'Username'}))
	password = forms.CharField(label="Password", max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','placeholder':'Password'}))

	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		
		user_qs = User.objects.filter(username=username)
		if user_qs.count() == 1:
			user = user_qs.first()
			if not user.is_active:
				raise forms.ValidationError("This account is not active,contact admin support to activate the account.")

		if not user:
			raise forms.ValidationError("Incorrect username or password entered!")

		if not user.check_password(password):
			raise forms.ValidationError("Incorrect username or password entered!")


		return super(UserLoginForm,self).clean(*args,**kwargs)

class MyRegistrationForm(UserCreationForm):
	group = forms.ModelChoiceField(label ='Account type:',queryset=Group.objects.all(),required=True,widget=forms.Select(attrs={'class':'form-control','name':'group'}))
	first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First name','name':'first_name'}))
	last_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','name':'last_name'}))
	username = forms.CharField(label="Username",max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username','name':'username'}))
	phone = forms.CharField(label="Phone number",max_length=15,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number  eg 254711222333'}))
	email = forms.CharField(max_length=75, required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'exampleInputEmail1','placeholder':'Enter your email','name':'email'}))
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Type in your password','name':'password1'}))
	password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repeat the password above','name':'password2'}))

	class Meta:
		model = User
		fields = ('group','first_name','last_name','username','phone','email')


	def clean_phone(self):
		if Profile.objects.filter(phone__iexact=self.cleaned_data['phone']):
			raise forms.ValidationError("Sorry ,this phone number is already in use.Please supply a different one.")
		if len(self.cleaned_data['phone'])<10:
			raise forms.ValidationError("This phone number is less than 10 digits.")
		if len(self.cleaned_data['phone'])>13:	
			raise forms.ValidationError("This phone number is more than expected size of 12 digits.")		
		if not ((self.cleaned_data['phone']).isdigit()):
			raise forms.ValidationError("This phone number is not in a valid format.Please exclude any characters or letters.Only numbers are allowed.")
		if self.cleaned_data['phone'].startswith('0'):
			raise forms.ValidationError("Sorry phone number must start with country code eg '2547xxxxxx'.")
		return self.cleaned_data['phone']
		
	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError("Sorry ,this email address is already in use.Please supply a different email address or request a password reset.")
		return self.cleaned_data['email']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Sorry the passwords you entered don't match.Please try again")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=("Email"), max_length=254,widget=forms.TextInput(attrs={'class':'passwordreset','name':'email'}))
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
