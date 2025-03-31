from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("wishlist/", views.view_wishlist),
    path("contact/", views.contactus_view, name="contact"),
    path(
        "products/<slug:pk>/", views.Productdetail, name="product_detail"
    ),  # Ensure <int:pk> matches the view
    path(
        "add-to-wishlist/<slug:item_id>/", views.add_to_wishlist, name="add_to_wishlist"
    ),
]
