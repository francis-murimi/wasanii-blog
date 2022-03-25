from django import forms
from .models import Order
from urllib import request

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone_number','delivery_point','area']