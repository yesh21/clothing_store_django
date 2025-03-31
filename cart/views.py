import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import Product
from .models import Cart, Order, OrderedItem
from django.db.models import Case, When
from django.contrib import messages


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
        print(pk_values)
        product_item_details = Product.objects.filter(pk__in=pk_values).order_by(
            Case(*[When(pk=pk, then=index) for index, pk in enumerate(pk_values)])
        )
        cart_items = list(cart_items.values())

    context = {"cart_product_items_details": zip(cart_items, product_item_details)}
    return render(request, "cart/html/cart.html", context=context)


def add_to_cart(request, product_id, quantity=1, action="add"):
    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)  # converts string to dict

    product = Product.objects.filter(product_id=product_id).first()

    if product_id not in cart and product:
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
    messages.success(request, "Added to cart")

    return response


@login_required
def view_order_details_by_id(request, order_ref):
    order_details = Order.objects.filter(order_id=order_ref).first()
    ordered_item_details = OrderedItem.objects.filter(order_id=order_ref)
    product_item_details = Product.objects.filter(
        pk__in=ordered_item_details.values_list("product", flat=True)
    )
    context = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
        "order_details": order_details,
        "ordered_product_item_details": zip(ordered_item_details, product_item_details),
    }
    return render(request, "html/order_details.html", context=context)
