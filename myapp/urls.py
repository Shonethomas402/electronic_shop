from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # User Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Product Browsing
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/phones/', views.phone_list, name='phone_list'),
    path('products/laptops/', views.laptop_list, name='laptop_list'),
    path('products/headsets/', views.headset_list, name='headset_list'),
    path('products/watches/', views.watch_list, name='watch_list'),

    # Category Browsing
    path('category/<str:category_name>/', views.category_search, name='category_search'),
    path('category/TV/', views.tv_list, name='tv_list'),

    # Shopping Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # Checkout and Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    # Reviews
    path('products/<int:product_id>/review/', views.add_review, name='add_review'),

    # Miscellaneous Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Admin Authentication and Dashboard
    path('custom_admin/login/', auth_views.LoginView.as_view(), name='custom_admin_login'),
    path('custom_admin/dashboard/', views.admin_dashboard, name='custom_admin_dashboard'),
    # Other custom admin paths...

    # Django Admin (default)
    # path('admin/', admin.site.urls),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
