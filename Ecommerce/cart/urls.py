"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cart import views
from django.urls import path
app_name="cart"
urlpatterns = [
        path('addtocart/<int:i>',views.AddToCart.as_view(),name="addtocart"),
        path('cart_view',views.CartView.as_view(),name="cart_view"),
        path('cart_decrement/<int:i>',views.CartDecrement.as_view(),name='cart_decrement'),
        path('cart_remove/<int:i>',views.CartRemove.as_view(),name="cart_remove"),
        path('checkout',views.Check_Out.as_view(),name="checkout"),
        path('payment',views.Payment.as_view(),name="payment"),
        path('success/<i>',views.Payment_Success.as_view(),name="pay_success"),
        path('your_order',views.YourOrder.as_view(),name="orders"),
]
