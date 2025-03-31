import uuid
from django.db import models
import string
import random
from django.conf import settings

# Create your models here.


def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(length))


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("tshirt", "T-Shirt"),
        ("jeans", "Jeans"),
        ("jacket", "Jacket"),
        ("shirt", "Shirt"),
        ("shorts", "Shorts"),
    ]
    product_id = models.CharField(
        primary_key=True, default=generate_random_string, max_length=50
    )
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=7, default="new")
    color_options = models.JSONField(default=dict(white="#ffffff"))
    images_files = models.FileField(upload_to="staticfiles//product_images/")
    images_files_back = models.FileField(upload_to="staticfiles//product_images/")
    is_avaliable = models.BooleanField(default=True)
    quantity_by_size = models.JSONField(
        default={"s": 0, "m": 0, "l": 0, "xl": 0, "xxl": 0}
    )
    catagory = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(
        max_length=500,
        default="Finest peice of colthing. Crafted from high-quality materials",
    )
    updated_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):

    # Unique reference for the order
    order_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)

    # Foreign Key linking to the User model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Status of the order
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("cancelled", "Cancelled"),
        ("delivered", "Delivered"),
        ("shipped", "Shipped"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.PositiveIntegerField()
    # Timestamps for creation and updates
    shipping_address = models.TextField()
    payment_info = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"


class OrderedItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.quantity} of {self.product.name} in Order {self.order_id.order_id}"
        )
