import json
from django.shortcuts import render
from django.http import HttpResponse

from core.models import Product
from .models import Cart

# Create your views here.


def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        product_item_details = Product.objects.filter(
            pk__in=cart_items.values_list("product", flat=True)
        )
    else:
        cart_items = request.COOKIES.get("cart", "{}")
        cart_items = json.loads(cart_items)
        pk_values = [key for key in cart_items.keys()]
        product_item_details = Product.objects.filter(pk__in=pk_values)

    context = {"cart_product_items_details": zip(cart_items, product_item_details)}
    return render(request, "cart/html/cart.html", context=context)


def add_to_cart(request, product_id, quantity=1, action="add"):
    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)  # converts string to dict

    if product_id not in cart:
        cart[product_id] = {"quantity": 0}

    if quantity == 1:
        if action == "subtract":
            quantity = int(cart[product_id]["quantity"]) - 1
        else:
            quantity = int(cart[product_id]["quantity"]) + 1

    if quantity < 0:
        cart.pop(str(product_id), None)

    if quantity > 10:
        quantity = 10

    if product_id in cart:
        cart[product_id]["quantity"] = quantity
    else:
        quantity = -1

    # Create response object
    response = HttpResponse(status=204)

    # Set the cookie with the updated wishlist
    response.set_cookie(
        "cart", json.dumps(cart), max_age=60 * 60 * 24 * 30
    )  # Cookie lasts for 30 days

    if request.user.is_authenticated:
        product = Product.objects.filter(product_id=product_id).first()
        cart_item = Cart.objects.filter(user=request.user, product=product).first()
        if cart_item:
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        else:
            if quantity > 0:
                Cart.objects.create(
                    user=request.user, product=product, quantity=quantity
                )
    return response
