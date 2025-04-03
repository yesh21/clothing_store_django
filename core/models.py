import uuid
from django.db import models
import string
import random
from django.conf import settings


def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(length))


# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7)  # For example: #FFFFFF

    def __str__(self):
        return self.name


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
    description = models.TextField(
        default="Finest peice of colthing. Crafted from high-quality materials",
    )
    is_avaliable = models.BooleanField(default=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=7, default="new")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    images_files = models.FileField(upload_to="staticfiles//product_images/")
    images_files_back = models.FileField(upload_to="staticfiles//product_images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductVariation(models.Model):
    product_variation_id = models.CharField(
        primary_key=True, default=generate_random_string, max_length=50
    )
    product = models.ForeignKey(
        Product, related_name="variations", on_delete=models.CASCADE
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    issued_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.color.name}"
