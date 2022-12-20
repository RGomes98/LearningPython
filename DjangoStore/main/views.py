from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Cart, Product, User
from django.urls import reverse
from datetime import timedelta

import requests
import datetime
import decimal
import locale


def registerPage(request):
    user = request.user
    register_form = UserCreationForm()

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        new_user = UserCreationForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(request, "main/error.html", {"error_message": new_user.errors})

    return render(request, "main/register.html", {"register_form": register_form})


def loginPage(request):
    user = request.user

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_session = authenticate(request, username=username, password=password)

        if user_session is not None:
            login(request, user_session)
            return redirect("home")
        else:
            return render(request, "main/error.html", {"error_message": "Wrong credentials!"})

    return render(request, "main/login.html", {})


def logoutUser(request):
    logout(request)
    return redirect("home")


def homePage(request):
    user = request.user

    try:
        products_data = requests.get("https://fakestoreapi.com/products").json()
    except:
        return render(request, "main/error.html", {"error_message": "FakeStoreAPI is down!"})

    if user.is_authenticated:
        Cart.objects.get_or_create(owner=user)

    return render(request, "main/home.html", {"products_data": products_data})


@login_required(login_url="login")
def cartPage(request):
    try:
        cart_id = request.user.cart.id
        cart = Cart.objects.filter(id=cart_id)[0]
    except:
        return redirect("home")

    products_count = cart.product_set.all().count()
    cart_products = cart.product_set.all().order_by("-quantity", "-added_at")

    for i in range(len(cart_products)):
        cart_products[i].price = cart_products[i].price * cart_products[i].quantity

    context = {"cart_products": cart_products, "products_count": products_count}
    return render(request, "main/cart.html", context)


@login_required(login_url="login")
def checkoutPage(request):
    try:
        cart_id = request.user.cart.id
        cart = Cart.objects.filter(id=cart_id)[0]
    except:
        return redirect("home")

    if not cart.product_set.all().count():
        return redirect("cart")

    SHIPPING_TIME = datetime.date.today() + timedelta(days=7)
    SHIPPING_TAX_AMMOUNT = 5
    PURCHASE_TAX_AMMOUNT = 2
    SUBTOTAL = 0

    cart_products = cart.product_set.all().order_by("-quantity", "-price")

    for i in range(len(cart_products)):
        cart_products[i].multiplied_price = cart_products[i].price * cart_products[i].quantity
        SUBTOTAL += cart_products[i].multiplied_price

    SHIPPING_PRICE = SUBTOTAL * SHIPPING_TAX_AMMOUNT / 100
    TAX_PRICE = (SHIPPING_PRICE + SUBTOTAL) * PURCHASE_TAX_AMMOUNT / 100
    TOTAL_PRICE = SHIPPING_PRICE + TAX_PRICE + SUBTOTAL
    ARRIVES_BY = SHIPPING_TIME.strftime("%a, %b %d")

    context = {"cart_products": cart_products, "arrives_by": ARRIVES_BY}

    def format_to_currency(SUBTOTAL, SHIPPING_PRICE, TAX_PRICE, TOTAL_PRICE):
        local_variables = locals()
        for i in local_variables:
            if isinstance(local_variables[i], decimal.Decimal):
                locale.setlocale(locale.LC_ALL, "en_US")
                context[i.lower()] = locale.format_string("%.2f", local_variables[i], True)

    format_to_currency(SUBTOTAL, SHIPPING_PRICE, TAX_PRICE, TOTAL_PRICE)

    return render(request, "main/checkout.html", context)


@login_required(login_url="login")
def addProduct(request, id):
    user_id = request.user.id
    cart_id = request.user.cart.id

    try:
        selected_product = requests.get(f"https://fakestoreapi.com/products/{id}").json()
    except:
        return render(request, "main/error.html", {"error_message": "Product not found!"})

    product, is_created = Product.objects.get_or_create(
        added_by=User(user_id),
        belongs_to=Cart(id=cart_id),
        name=selected_product["title"],
        image=selected_product["image"],
        price=selected_product["price"],
        description=selected_product["description"],
    )

    if not is_created:
        product.quantity += 1
        product.save()

    return redirect("cart")


@login_required(login_url="login")
def removeProduct(request, id):
    cart_id = request.user.cart.id

    try:
        product = Product.objects.filter(id=id, belongs_to=cart_id)[0]
    except:
        return render(request, "main/error.html", {"error_message": "Product not found!"})

    product.delete()

    return redirect("cart")


@login_required(login_url="login")
def addQuantity(request, id):
    cart_id = request.user.cart.id

    try:
        product = Product.objects.filter(id=id, belongs_to=cart_id)[0]
    except:
        return render(request, "main/error.html", {"error_message": "Product not found!"})

    product.quantity += 1
    product.save()

    return redirect("cart")


@login_required(login_url="login")
def removeQuantity(request, id):
    cart_id = request.user.cart.id

    try:
        product = Product.objects.filter(id=id, belongs_to=cart_id)[0]
    except:
        return render(request, "main/error.html", {"error_message": "Product not found!"})

    if product.quantity == 1:
        return redirect(reverse("remove-product", args=[id]))
    else:
        product.quantity -= 1
        product.save()

    return redirect("cart")


@login_required(login_url="login")
def finishTransactionPage(request):
    try:
        cart_id = request.user.cart.id
        cart_products = Product.objects.filter(belongs_to=cart_id)
    except:
        return redirect("home")

    if cart_products.count():
        cart_products.delete()
        return render(request, "main/finish.html", {})
    else:
        return redirect("cart")
