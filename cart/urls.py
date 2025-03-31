from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.cart),
    path(
        "addcart/<slug:product_id>/<int:quantity>/<slug:action>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "order-details/<slug:order_ref>/",
        views.view_order_details_by_id,
        name="order-details-by-id",
    ),
]
