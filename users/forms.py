from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password'})
        }


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_line_1','address_line_2','city','state','zip_code','country','mobile_number','alternative_mobile_number')
        widgets = {
            'address_line_1': forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control'}),
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class':'form-control'}),
            'alternative_mobile_number': forms.TextInput(attrs={'class':'form-control'})
        }