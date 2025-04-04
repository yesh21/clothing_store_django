import json
from django.shortcuts import render
from django.db.models import Q
from core.models import Category, Color, Product, ProductVariation, Size
from login.models import Profile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .forms import ProductFilterForm
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.contrib import messages


# Create your views here.
def sort_by_option(sort_by, products):
    if sort_by == "price_asc":
        products = products.order_by("discounted_price")
    elif sort_by == "price_desc":
        products = products.order_by("-discounted_price")
    elif sort_by == "date_added":
        products = products.order_by("-updated_at")
    else:
        products = products  # Default sorting
    return products


def index(request):
    wishlist_cookie = request.COOKIES.get("wishlist", "")
    # Split the string by a delimiter (e.g., comma)
    wishlist_values = wishlist_cookie.split(",")
    sort_by = request.GET.get("sort_by", "")
    products = Product.objects.all()
    products = sort_by_option(sort_by, products)

    return render(
        request,
        "html/index.html",
        {"products": products, "wishlistcookie": wishlist_values},
    )


def wishlist(request):
    return render(request, "html/wishlist.html")


def Productdetail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Use pk instead of id

    colors = Color.objects.filter(productvariation__product_id=pk).distinct()

    # Get distinct sizes
    sizes = Size.objects.filter(productvariation__product_id=pk).distinct()

    context = {
        "product": product,
        "colors": colors,
        "sizes": sizes,
    }
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


def get_product_variation_json(request, product_id, size, color):
    response_data = {"stock_quantity": 0, "message": "sorry couldn't find item"}
    product_variations = ProductVariation.objects.filter(
        product=product_id, size=size, color=color
    ).first()

    if product_variations:
        serialized_data = serialize("json", [product_variations])
        # Parse the serialized data
        response_data = json.loads(serialized_data)[0]

    return JsonResponse(response_data)


def search_products(request):
    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(variations__color__name__icontains=query)
            | Q(variations__size__name__icontains=query)
            | Q(variations__sku=query)
        ).distinct()
    else:
        products = Product.objects.all()
    sort_by = request.GET.get("sort_by", "")
    products = sort_by_option(sort_by, products)
    return render(
        request,
        "html/product_listing_page.html",
        {"products": products, "query": query},
    )


def product_by_category(request, category_id, name="collection"):
    category = get_object_or_404(Category, category_id=category_id)
    products = category.product_set.all()  # Use default reverse relation
    sort_by = request.GET.get("sort_by", "")
    products = sort_by_option(sort_by, products)
    return render(
        request,
        "html/product_listing_page.html",
        {"category": category, "products": products},
    )


def ajax_messages(request):

    # Retrieve all messages
    django_messages = []
    system_messages = messages.get_messages(request)
    system_messages.used = True

    for message in system_messages:
        django_messages.append(
            {
                "level": message.level,
                "message": message.message,
                "tags": message.tags,
            }
        )
    return JsonResponse({"messages": django_messages})
