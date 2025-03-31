from django.contrib import admin
from core.models import Product, Order, OrderedItem


# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderedItem)
