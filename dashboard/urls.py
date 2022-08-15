from django.urls import path
from . import views
from .views import (
    ItemListView,
    ItemDetailView,
    AddToCartView,
    ProductDetailView,
    MyCartView,
    ManageCartView,
    EmptyCartView,
    CheckoutView,
    AdminDashView,
    OrderDetailView,
    ChangeStatusView
)


urlpatterns = [
    path('index/', views.index, name='index'),##check
    path('admins/', views.admins, name= 'admins'),##check
    path('products/', views.products , name= 'products'),##check
    path('delete/<int:key>', views.delete, name= 'delete'),##check
    path('update/<int:key>', views.update, name='update'),##check
    path('items_list/', ItemListView.as_view(), name='items_list'),##check
    path('my_cart/', MyCartView.as_view(), name='my_cart'),##check
    path('make_order/<slug:slug>/', ItemDetailView.as_view(), name='make_order'),##check
    path('add_to_cart/<int:pro_id>/', AddToCartView.as_view(), name='add_to_cart'),##check
    path("manage_cart/<int:cp_id>/", ManageCartView.as_view(), name="manage_cart"),
    path("empty_cart/", EmptyCartView.as_view(), name="empty_cart"),##check
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("admin_dash/", AdminDashView.as_view(), name="admin_dash"),
    path("order_detail/<int:pk>/", OrderDetailView.as_view(),
         name="order_detail"),
    path("order_detail-<int:pk>-change/",
         ChangeStatusView.as_view(), name="change_status"),
    path('order_summary/<slug:slug>/', ProductDetailView.as_view(), name='order_summary'),##check
    
   
]