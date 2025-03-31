import uuid
from django.conf import settings
from django.db import models
from core.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Foreign key to User model
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Foreign key to Product model
    quantity = models.PositiveIntegerField(
        default=1
    )  # Quantity of the product in the cart
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the cart item was created
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Timestamp when the cart item was last updated

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        unique_together = (
            "user",
            "product",
        )  # Ensure a user can only have one of each product in their cart

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (Quantity: {self.quantity})"


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
