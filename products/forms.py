from django import forms
from .models import Cart, Orders

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user_id','product_id','cart_quantity')


class OrdersForm(forms.ModelForm):
    
    class Meta:
        model = Orders
        fields = ('user_id','product_id','quantity','address','mobile')
