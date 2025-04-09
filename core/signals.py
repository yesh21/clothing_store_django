# inventory/signals.py
from django.dispatch import receiver
from cart.signals import order_confirmed
from .models import ProductVariation  # Your inventory model


@receiver(order_confirmed)
def update_inventory(sender, order, **kwargs):
    for item in order.items.all():
        try:
            stock_item = ProductVariation.objects.get(
                product_variation_id=item.product_variation
            )
            stock_item.stock_quantity -= item.quantity
            stock_item.save()
        except ProductVariation.DoesNotExist:
            # Handle missing inventory items
            pass
