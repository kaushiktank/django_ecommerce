from django import forms
from django.db import models
from .models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user_id','product_id','cart_quantity')
