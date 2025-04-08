from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path(
        "addcart/<slug:product_variation_id>/<int:quantity>/<slug:action>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "order-details/<slug:order_ref>/",
        views.view_order_details_by_id,
        name="order-details-by-id",
    ),
    path(
        "delivery/availability/",
        views.check_delivery_availability,
        name="delivery_availability",
    ),
    path("pay/<slug:amount>/<slug:transactionid>/", views.pay, name="pay"),
    path(
        "payment-response/",
        views.payment_response,
        name="payment_response",
    ),
]
