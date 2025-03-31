from django.shortcuts import render
from core.models import Product, OrderedItem, Order
from login.models import Profile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import ProductFilterForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    wishlist_cookie = request.COOKIES.get("wishlist", "")
    # Split the string by a delimiter (e.g., comma)
    wishlist_values = wishlist_cookie.split(",")
    products = Product.objects.all()

    if request.method == "GET":
        form = ProductFilterForm(request.GET)

        if form.is_valid():
            category = form.cleaned_data.get("category")
            size = form.cleaned_data.get("size")
            color = form.cleaned_data.get("color")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")

            # if category:
            #     products = products.filter(category=category)
            # if size:
            #     products = products.filter(size=size)
            # if color:
            #     products = products.filter(
            #         color__icontains=color
            #     )  # Case-insensitive search
            if min_price is not None:
                products = products.filter(discounted_price__gte=min_price)
            if max_price is not None:
                products = products.filter(discounted_price__lte=max_price)

    else:
        form = ProductFilterForm()

    return render(
        request,
        "html/index.html",
        {"products": products, "form": form, "wishlistcookie": wishlist_values},
    )


def wishlist(request):
    return render(request, "html/wishlist.html")


def Productdetail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Use pk instead of id
    context = {"product": product}
    return render(request, "html/product_by_id.html", context)


def error_404_view(request, exception):

    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, "html/404.html")


def contactus_view(request):
    return render(request, "html/contact_us.html")


def add_to_wishlist(request, item_id):
    # Get the current wishlist from cookies or create an empty list
    wishlist = request.COOKIES.get("wishlist", "")
    if wishlist:
        # Convert the string of IDs into a list
        wishlist = wishlist.split(",")
    else:
        wishlist = []

    # Add the new item if it's not already in the wishlist
    if str(item_id) not in wishlist:
        wishlist.append(str(item_id))
    else:
        wishlist.remove(str(item_id))

    # Convert the list back to a string
    wishlist_str = ",".join(wishlist)

    # Create response object
    response = HttpResponse(status=204)

    # Set the cookie with the updated wishlist
    response.set_cookie(
        "wishlist", wishlist_str, max_age=60 * 60 * 24 * 30
    )  # Cookie lasts for 30 days

    if request.user.is_authenticated:
        record, created = Profile.objects.get_or_create(
            user_id=request.user,
        )
        if not created:
            record.wishlist_items = wishlist
            record.save()
    return response


def view_wishlist(request):
    # Retrieve the wishlist from cookies
    wishlist = request.COOKIES.get("wishlist", "")

    if wishlist:
        items = wishlist.split(",")
        product_list = Product.objects.filter(pk__in=items)
        return render(
            request, "html/wishlist.html", context={"products_wishlist": product_list}
        )

    return render(request, "html/wishlist.html", {"items": []})


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
