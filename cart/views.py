import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import ProductVariation, Product
from .models import Cart, Order, OrderedItem
from django.db.models import Case, When
from django.contrib import messages


# Create your views here.


def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        product_variation_details = ProductVariation.objects.filter(
            pk__in=cart_items.values_list("product_variation", flat=True)
        )
    else:
        cart_items = request.COOKIES.get("cart", "{}")
        cart_items = json.loads(cart_items)
        pk_values = [key for key in cart_items.keys()]
        product_variation_details = ProductVariation.objects.filter(
            pk__in=pk_values
        ).order_by(
            Case(*[When(pk=pk, then=index) for index, pk in enumerate(pk_values)])
        )

        missing_keys = set(pk_values) - set(
            list(product_variation_details.values_list("pk", flat=True))
        )

        for key in missing_keys:
            cart_items.pop(key, None)  # Removes missing items

        cart_items = list(cart_items.values())

    context = {"cart_product_items_details": zip(cart_items, product_variation_details)}
    return render(request, "cart/html/cart.html", context=context)


def add_to_cart(request, product_variation_id, quantity=1, action="add"):
    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)  # converts string to dict

    product_variation = ProductVariation.objects.filter(
        product_variation_id=product_variation_id
    ).first()

    if product_variation_id not in cart and product_variation:
        cart[product_variation_id] = {"quantity": 0}

    if quantity == 1:
        if action == "subtract":
            quantity = int(cart[product_variation_id]["quantity"]) - 1
        else:
            quantity = int(cart[product_variation_id]["quantity"]) + 1

    if quantity < 0:
        cart.pop(str(product_variation_id), None)

    if quantity > 10:
        quantity = 10

    if product_variation_id in cart:
        cart[product_variation_id]["quantity"] = quantity
    else:
        quantity = -1
    # Create response object
    response = HttpResponse(status=204)

    # Set the cookie with the updated wishlist
    response.set_cookie(
        "cart", json.dumps(cart), max_age=60 * 60 * 24 * 30
    )  # Cookie lasts for 30 days

    if request.user.is_authenticated:

        cart_item = Cart.objects.filter(
            user=request.user, product_variation=product_variation
        ).first()
        if cart_item:
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        else:
            if quantity > 0 and product_variation:
                Cart.objects.create(
                    user=request.user,
                    product_variation=product_variation,
                    quantity=quantity,
                )
    messages.success(request, "Added to cart")

    return response


@login_required
def view_order_details_by_id(request, order_ref):
    order_details = Order.objects.filter(order_id=order_ref).first()
    ordered_item_details = OrderedItem.objects.filter(order_id=order_ref)
    product_item_details = ProductVariation.objects.filter(
        pk__in=ordered_item_details.values_list("product_variation", flat=True)
    )
    context = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
        "order_details": order_details,
        "ordered_product_item_details": zip(ordered_item_details, product_item_details),
    }
    return render(request, "html/order_details.html", context=context)
