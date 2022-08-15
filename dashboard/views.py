from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ProductForm, CheckoutForm
from django.contrib import messages
from django.views.generic import DetailView, View,FormView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#force login first before gaining access to pages
@login_required(login_url='login')
def index(request):
    return render(request, 'skeleton/index.html' )

@login_required(login_url='login')
def admins(request):
    return render(request, 'skeleton/admins.html' )




@login_required(login_url='login')
def products(request):
    #fetching all the data in the products table
    #stocks = Product.objects.raw('SELECT * FROM dashboard_product')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'{title} has been added')
            return redirect('products')
    else:
        form = ProductForm()
   
    context = {
        'stocks': Product.objects.all(),
        'form':form
    }
    return render(request, 'skeleton/products.html', context)

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

# view product for customer
class ItemListView( TemplateView):
    template_name ='skeleton/items_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.all().order_by("-id")
        context['product_list'] = product_list
        return context
        

#view item details for customer
class ItemDetailView(TemplateView):
    template_name ='skeleton/make_order.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug= url_slug)
        product.view_count +=1
        product.save()
        context['product'] = product
        return context
        
#make order
class AddToCartView(TemplateView):
    template_name ='skeleton/add_to_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ## get id form url
        product_id = self.kwargs['pro_id']
        ## getting the product
        product_obj =Product.objects.get(id=product_id)
        
        #check if the cart is empty
        cart_id = self.request.session.get('card_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product = product_id
            )
            
                        # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()
        return context
    
    
##view products in cart
class MyCartView(TemplateView):
    template_name = "skeleton/my_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
    
    
### place the order and submit
class CheckoutView(CreateView):
    template_name = "skeleton/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("items_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            order = form.save()
        return super().form_valid(form)
    
    
    
class ChangeStatusView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("order_detail", kwargs={"pk": order_id}))




##customer order summary
class ProductDetailView(DetailView):
    template_name ='skeleton/order_summary.html'
    model = Order
    context_object_name = 'ord_obj'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context



### add||remove ||reduce quantity
class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj
            cp_obj.save()
            cart_obj.total += cp_obj
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj
            cp_obj.save()
            cart_obj.total -= cp_obj
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("my_cart")

### remove items added to cart
class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("my_cart")
    
    
    
    
    
class AdminDashView(TemplateView):
    template_name = "skeleton/admin_dash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context


class OrderDetailView(DetailView):
    template_name = "skeleton/order_detail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context



#update stock
@login_required(login_url='login')
def update(request, key):
    stock = Product.objects.get(id=key)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=stock)
    context= {
        'form': form,
    }
    return render(request, 'skeleton/update.html', context)

#delete stock form database
@login_required(login_url='login')
def delete(request, key):
    stock = Product.objects.get(id=key)
    if request.method == 'POST':
        stock.delete()
        return redirect('products')
    return render(request, 'skeleton/delete.html')


