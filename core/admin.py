from django.contrib import admin
from core.models import Category, Product, Brand, ProductVariation, Size, Color


# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductVariation)
