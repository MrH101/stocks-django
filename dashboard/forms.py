from django import forms
from .models import Product, Order


#create form to add products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =[
            'title',
            'category',
            'stock_quantity',
            'price',
            'expiry_date',
            ]
        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email", "payment_method"]