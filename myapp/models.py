from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Products Table
class Product(models.Model):
    name = models.CharField("Product Name", max_length=20)
    description = models.TextField("Description", null=True, blank=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Stock")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image_url = models.URLField("Image URL", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Orders Table
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField("Total Price", max_digits=10, decimal_places=2)
    status = models.CharField(
        "Order Status",
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='pending',
    )

    shipping_address = models.CharField("Shipping Address", max_length=50, null=True, blank=True)
    billing_address = models.CharField("Billing Address", max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

# Order Items Table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantity")
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id} - {self.product.name}"

# Reviews Table
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField("Rating")
    review_text = models.TextField("Review", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - {self.product.name}"

# Discounts Table
class Discount(models.Model):
    code = models.CharField("Discount Code", max_length=10, unique=True)
    discount_type = models.CharField(
        "Discount Type",
        max_length=15,
        choices=[
            ('percentage', 'Percentage'),
            ('fixed_amount', 'Fixed Amount'),
        ],
    )
    value = models.DecimalField("Value", max_digits=10, decimal_places=2)
    expiry_date = models.DateField("Expiry Date", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.email}"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
