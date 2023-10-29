from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class CreateUserForm(UserCreationForm):
    """
    Form for creating a new user.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 
                  'password1', 'password2']


class ProfileForm(ModelForm):
    """
    Form for creating/editing a user profile.
    """
    class Meta:
        model = Profile
        fields = ['address', 'phone_number', 'bio', 'balance', 'image']


class LoginForm(AuthenticationForm):
    """
    Form for user authentication.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}
        )
    )


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UpdateProfileForm(forms.ModelForm):
    """
    Form for updating profile details.
    """

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'bio', 'balance', 'image']
