from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

#admin and customer models
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

#Products model
class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(unique= True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    stock_quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(null=True)
    expiry_date =models.DateTimeField(null=True)
    view_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
       # return reverse("make_order", kwargs={
      #      "slug": self.slug
       # })
        
   # def get_add_to_orders_url(self):
     #   return reverse("add_to_orders", kwargs={
    #        "slug": self.slug
    #    })
    
    
#Orders Model
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(null= True, auto_now_add=True)
    ordered= models.BooleanField(default=False)
    
    def __str__(self):
        return 'cart: ' + str(self.id)
    
   # def get_total(self):
    #    total = 0
     #   for order_item in self.items.all():
      #      total += order_item.get_final_price()
       # return total
    
     
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(null=True,blank=True)
    ordered =models.BooleanField(default=False)
    
    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)
    
    #calculate total price
   # def get_total_order_price(self):
    #    return self.quantity * self.item.price
    
    # def get_final_price(self):
      #  return self.get_total_order_price()
    
ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True,blank=True)
    ordered_by = models.CharField(max_length=200,null=True,blank=True)
    shipping_address = models.CharField(max_length=200,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True,blank=True)
    total = models.PositiveIntegerField(null=True,blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")

    def __str__(self):
        return "Order: " + str(self.id)

    
    

