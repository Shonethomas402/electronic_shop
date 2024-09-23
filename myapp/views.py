from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, Review, Category, Discount  # Ensure all models are imported
from .forms import UserRegistrationForm, ReviewForm  # Import necessary forms
from django.http import Http404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User

# Home View
def home(request): 
    products = Product.objects.all()
    return render(request, 'home.html')

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# User Profile View
@login_required
def profile(request):
    return render(request, 'user_dashboard.html')

# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product Detail View
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})

# Cart Views
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'items': items, 'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, "Cart updated.")
    return redirect('cart')

# Checkout View
@login_required
def checkout(request):
    # Implement checkout logic here
    return render(request, 'checkout.html')

# Order Views
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, 'order_detail.html', {'order': order})

# Review View
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully.")
            return redirect('product_detail', pk=product_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})

# Miscellaneous Pages
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Notification View
def notifications(request):
    return render(request, 'notifications.html')

# Category and Product Views
def category_search(request, category_name):
    products = Product.objects.filter(category_name_iexact=category_name)
    if not products.exists():
        raise Http404("No Category matches the given query.")
    return render(request, 'category_search.html', {'category': category_name, 'products': products})

def tv_list(request):
    products = Product.objects.filter(category='TV')
    return render(request, 'category_search.html', {'category': 'TV', 'products': products})

def phone_list(request):
    products = Product.objects.filter(category='Phone')
    return render(request, 'myapp/phone_list.html', {'products': products})

def laptop_list(request):
    products = Product.objects.filter(category='Laptop')
    return render(request, 'myapp/laptop_list.html', {'products': products})

def headset_list(request):
    products = Product.objects.filter(category='Headset')
    return render(request, 'myapp/headset_list.html', {'products': products})

def watch_list(request):
    products = Product.objects.filter(category='Watch')
    return render(request, 'myapp/watch_list.html', {'products': products})

# Admin Dashboard Views
def admin_dashboard(request):
    total_sales = Order.objects.filter(status='Completed').count()
    total_users = User.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        'total_sales': total_sales,
        'total_users': total_users,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_dashboard.html', context)

# User Management Views
class UserListView(ListView):
    model = User
    template_name = 'user_list.html'

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'user_form.html'

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'user_form.html'

class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = '/admin/users/'

# Category Management View
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'

# Product Management View
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'category', 'image']
    template_name = 'product_form.html'

# Order Management Views
class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'order_form.html'

# Inventory Management View
def inventory_management(request):
    low_stock_products = Product.objects.filter(stock__lt=10)
    return render(request, 'inventory.html', {'low_stock_products': low_stock_products})

# Discount Management View
class DiscountCreateView(CreateView):
    model = Discount
    fields = ['code', 'discount_percentage', 'expiration_date']
    template_name = 'discount_form.html'

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def manage_categories(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'manage_categories.html', {'categories': categories})

def manage_products(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'manage_products.html', {'products': products})
def manage_orders(request):
    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'manage_orders.html', {'orders': orders})

def manage_discounts(request):
    discounts = Discount.objects.all()  # Fetch all discounts
    return render(request, 'manage_discounts.html', {'discounts': discounts})

def dashboard_view(request):
    return render(request, 'dashboard.html')
