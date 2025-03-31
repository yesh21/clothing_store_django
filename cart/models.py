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
