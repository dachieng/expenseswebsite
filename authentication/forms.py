from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email :", widget=forms.EmailInput(
        attrs={'placeholder': 'Enter Email'}))
    username = forms.CharField(label="Username :", widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username'}))
    password1 = forms.CharField(label="Password : ", required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))

    password2 = forms.CharField(label="Password Confirmation: ", required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Your Password'}))

    class Meta:
        model = User
        fields = ['username', 'email',  'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'occupation', 'age']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
