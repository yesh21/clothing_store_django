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
    path(
        "get-product-variation-json/<slug:product_id>/<slug:size>/<slug:color>/",
        views.get_product_variation_json,
        name="get_product_variation_json",
    ),
    path("search/", views.search_products, name="search_products"),
    path(
        "categories/<slug:category_id>/<slug:name>/",
        views.product_by_category,
        name="product_by_category",
    ),
]
