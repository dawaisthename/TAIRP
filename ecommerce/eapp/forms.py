from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from .models import *


class CustomerRegisterForm(UserCreationForm):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
class UserUpdateForm(forms.ModelForm):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','phone','address']