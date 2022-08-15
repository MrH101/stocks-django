from django.contrib import admin
from .models import Product, Order, Cart, CartProduct, Customer, Admin

admin.site.site_header = 'Stock Dashboard'

#create display table in admin dashboard

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock_quantity', 'price', 'expiry_date', 'category')
    list_filter = ['category',]

# Register your models here.

admin.site.register(Product, ItemAdmin)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Admin)
