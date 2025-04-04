import base64
from datetime import datetime
import hashlib
import json
from uuid import uuid4
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from cart.forms import AddressForm
from core.models import ProductVariation, Product
from .models import Cart, Order, OrderedItem
from django.db.models import Case, When
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import jsons
import base64
import requests
import shortuuid

# Create your views here.


def get_cart_product_items_details(request):
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
            cart_items.pop(key, None)  # Removes missing items in wishlist cookie
        cart_items = list(cart_items.values())

    return zip(cart_items, product_variation_details)


def calculate_billing_info(cart_product_items_details):
    # Initialize billing details
    subtotal = 0
    subtotal_without_discount = 0
    total_quantity = 0

    # Calculate subtotal and total quantity
    for cart_item, product_variety in cart_product_items_details:
        if isinstance(cart_item, dict):
            cart_item_quantity = cart_item["quantity"]
        else:
            cart_item_quantity = cart_item.quantity
        line_total = product_variety.selling_price * cart_item_quantity
        line_total_without_discount = product_variety.issued_price * cart_item_quantity
        subtotal += line_total
        subtotal_without_discount += line_total_without_discount
        total_quantity += cart_item_quantity

    # Apply any additional charges (e.g., taxes, shipping fees)
    tax_rate = 0.10  # Example: 10% tax
    shipping_fee = 0.00  # Example: Fixed shipping fee
    tax = float(subtotal) * tax_rate
    total = float(subtotal) + tax + shipping_fee
    total_saved = float(subtotal_without_discount) - float(subtotal)

    # Context for rendering the billing information
    context = {
        "subtotal": float(subtotal),
        "tax": round(tax, 2),
        "total_saved": total_saved,
        "shipping_fee": shipping_fee,
        "total": total,
        "total_quantity": total_quantity,
    }
    return context


def cart(request):
    cart_product_items_details = get_cart_product_items_details(request)
    billing_details = calculate_billing_info(cart_product_items_details)
    cart_product_items_details = get_cart_product_items_details(request)
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            # Process the valid data (e.g., save to database)
            cleaned_data = form.cleaned_data
            url = reverse(
                "cart:delivery_availability", kwargs={"address": "cleaned_data"}
            )  # Resolves the named URL

            return redirect(url)  # Redirect to a success page
    else:
        form = AddressForm()

    return render(
        request,
        "cart/html/cart.html",
        context={
            "cart_product_items_details": cart_product_items_details,
            "billing_details": billing_details,
            "form": form,
        },
    )


def add_to_cart(request, product_variation_id, quantity=1, action="add"):
    err_flag = 0
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
    if product_variation.stock_quantity < quantity:
        quantity = product_variation.stock_quantity
        messages.info(request, "OOPs, low inventory")
        err_flag = 1

    if product_variation_id in cart:
        cart[product_variation_id]["quantity"] = quantity
    else:
        messages.info(request, "Error while adding")
        quantity = -1
        err_flag = 1
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
    if not err_flag:
        messages.success(request, "Added to cart")

    return response


def ajax_messages(request):

    # Retrieve all messages
    django_messages = []
    system_messages = messages.get_messages(request)

    for message in system_messages:
        django_messages.append(
            {
                "level": message.level,
                "message": message.message,
                "tags": message.tags,
            }
        )
    system_messages.used = True
    return JsonResponse({"messages": django_messages})


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


def check_delivery_availability(request, address):
    # Example delivery times and cutoffs
    delivery_times = {"5pm": "16:00", "8pm": "20:00", "midnight": "00:00"}
    cutoffs = {"5pm": "16:00", "8pm": "19:00", "midnight": "23:00"}

    current_time = datetime.now().strftime("%H:%M")
    delivery_info = {}

    for time, cutoff in cutoffs.items():
        if current_time < cutoff:
            delivery_info[time] = "Available"
        else:
            delivery_info[time] = "Not Available"

    cart_product_items_details = get_cart_product_items_details(request)
    billing_details = calculate_billing_info(cart_product_items_details)
    cart_product_items_details = get_cart_product_items_details(request)

    return render(
        request,
        "cart/html/delivery_availability.html",
        {
            "delivery_info": delivery_info,
            "cart_product_items_details": cart_product_items_details,
            "billing_details": billing_details,
        },
    )


def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode("utf-8"))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode("utf-8")
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode("utf-8")


def pay(request):
    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT86",
        "merchantTransactionId": shortuuid.uuid(),
        "merchantUserId": "MUISD123",
        "amount": 10000,
        "redirectUrl": "http://127.0.0.1:8000/payment-response/",
        "redirectMode": "POST",
        "callbackUrl": "http://127.0.0.1:8000/payment-response/",
        "mobileNumber": "9999999999",
        "paymentInstrument": {"type": "PAY_PAGE"},
    }
    INDEX = "1"
    SALT_ENDPOINT = "/pg/v1/pay"
    SALTKEY = "96434309-7796-489d-8924-ab56988a6076"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + SALT_ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + "###" + INDEX
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # # Payload Send
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": checkSum,
        "accept": "application/json",
    }
    json_data = {
        "request": base64String,
    }
    response = requests.post(
        "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay",
        headers=headers,
        json=json_data,
    )
    responseData = response.json()
    print(responseData)
    return redirect(responseData["data"]["instrumentResponse"]["redirectInfo"]["url"])


@csrf_exempt
def payment_response(request):
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    SALTKEY = "96434309-7796-489d-8924-ab56988a6076"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Access form data in a POST request
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data = request.POST
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert form data to a dictionary
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data_dict = dict(form_data)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    transaction_id = form_data.get("transactionId", None)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 1.In the live please match the amount you get byamount you send also so that hacker can't pass static value.
    # 2.Don't take Marchent ID directly validate it with yoir Marchent ID
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if transaction_id:
        request_url = (
            "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/"
            + transaction_id
        )
        sha256_Pay_load_String = (
            "/pg/v1/status/PGTESTPAYUAT/" + transaction_id + SALTKEY
        )
        sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + "###" + INDEX
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Payload Send
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": checksum,
            "X-MERCHANT-ID": transaction_id,
            "accept": "application/json",
        }
        response = requests.get(request_url, headers=headers)
        # page_respond_data=form_data_dict, page_respond_data_varify=response.text
    return render(
        request,
        "cart/html/payment_response.html",
        {"output": response.text, "main_request": form_data_dict},
    )
