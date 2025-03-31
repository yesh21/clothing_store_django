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
]
