from django.urls import path
from . import views


urlpatterns = [
    path("", views.homePage, name="home"),
    path("cart/", views.cartPage, name="cart"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("checkout/", views.checkoutPage, name="checkout"),
    path("add-product/<int:id>/", views.addProduct, name="add-product"),
    path("add-quantity/<int:id>/", views.addQuantity, name="add-quantity"),
    path("remove-product/<int:id>/", views.removeProduct, name="remove-product"),
    path("purchase-history/", views.purchaseHistoryPage, name="purchase-history"),
    path("remove-quantity/<int:id>/", views.removeQuantity, name="remove-quantity"),
    path("finish-transaction/", views.finishTransactionPage, name="finish-transaction"),
]
