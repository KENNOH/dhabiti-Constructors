from django.contrib.auth.forms import UserChangeForm
import time
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.models import Group
from accounts.models import specialization
from .models import Service 


class UpdateProfile(UserChangeForm):
	first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'name': 'first_name'}))
	last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'name': 'last_name'}))
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Enter your username', 'name': 'username'}))
	email = forms.CharField(max_length=75, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'exampleInputEmail1', 'placeholder': 'Enter your email', 'name': 'email'}))
	display_pic = forms.ImageField(required=False)
	
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',
		          'password', 'display_pic')


class ServiceForm(forms.ModelForm):
    Type = forms.ModelChoiceField(label="Select Pet type:", required=True, queryset=specialization.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'name': 'Type'}))
    #attachment = forms.ImageField(label="Attachment:", required=True, widget=forms.ClearableFileInput(attrs={'multiple': False, 'name': 'attachment'}))
    attachment2 = forms.ImageField(label="Attachment:", required=True, widget=forms.ClearableFileInput(attrs={'multiple': True, 'name': 'attachment2'}))
    #contact_email = forms.CharField(label='Contact Email:', max_length=200, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    #contact_phone = forms.CharField(label='Contact Phone:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    description = forms.CharField(label="Any Message?:", required=False, max_length=200, widget=forms.Textarea(attrs={'class': 'form-control form-textbox', 'name': 'description', 'rows': '4'}))
    location = forms.CharField(label='Location:', max_length=200, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    cost = forms.CharField(label='cost:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))

    class Meta:
        model = Service
        fields = ('Type', 'location','cost','description')
    
    def clean(self, *args, **kwargs):
        # contact_email = self.cleaned_data['contact_email']
        # if not contact_email:
        #     raise forms.ValidationError("Please a contact email.")
        return super(ServiceForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        Document = super(ServiceForm, self).save(commit=False)
        if commit:
            Document.save()
        return Document


class DateInput(forms.DateTimeInput):
	input_type = 'date'

class BookForm(forms.Form):
    start_date = forms.DateField(required=True, label="Expected date to start working:", widget=DateInput(attrs={'class': 'form-control form-textbox'}))
    message = forms.CharField(label="Leave a Message:", required=False, max_length=200, widget=forms.Textarea(
    	attrs={'class': 'form-control form-textbox', 'name': 'description', 'rows': '4'}))


    class Meta:
        fields = ('start_date', 'message')

    def clean(self, *args, **kwargs):
        # contact_email = self.cleaned_data['contact_email']
        # if not contact_email:
        #     raise forms.ValidationError("Please a contact email.")
        return super(BookForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        Document = super(BookForm, self).save(commit=False)
        if commit:
            Document.save()
        return Document
