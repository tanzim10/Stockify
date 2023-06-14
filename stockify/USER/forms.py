from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['address','phone_number','bio','image']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True,'class': 'form-control'}))
    password = forms.CharField(
        label = "Password",
        strip= False,
        widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-comtrol'})        
    )


class User_UpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField() 
    email = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class Update_ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields =['phone_number','address','bio','image']

