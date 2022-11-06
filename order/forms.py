from django import forms
from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =[
            'first_name','last_name','phone_number',
            'email','address_line1','address_line2',
            'city','state','country','order_note'  ,
        ]

