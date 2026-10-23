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

from django.urls import path
from shop import views
app_name="shop"
urlpatterns = [
    path('',views.CategoryView.as_view(),name="category"),
    path('detail/<int:i>',views.Product_View.as_view(),name="products"),
    path('product_detail/<int:i>',views.Product_detail.as_view(),name="p_detail"),
    path('adminhome',views.AdminHome.as_view(),name="admin_home"),
    path('signup',views.SignUpView.as_view(),name="signup"),
    path('login/',views.UserLogin.as_view(),name="user_login"),
    path('logout',views.LogoutView.as_view(),name="user_logout"),
    path('add_category',views.AddCategory.as_view(),name="add_category"),
    path('add_product',views.AddProduct.as_view(),name="add_product"),
    path('addstock/<int:i>',views.AddStock.as_view(),name="add_stock"),

]
