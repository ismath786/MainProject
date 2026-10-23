
from django.shortcuts import render, redirect
from django.views import View
from shop.models import Category,Product
from shop.forms import SignupForm,LoginForms,CategoryForm,ProductForm,StockForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'categories':c})
class Product_View(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        return render(request,'product.html',{'category':c})
class Product_detail(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        return render(request,'product_detail.html',{'product':p})
class AdminHome(View):
    def get(self,request):
        return render(request,'admin_home.html')
class SignUpView(View):
    def get(self,request):
        form_instance=SignupForm()
        return render(request,'signup.html',{'form':form_instance})
    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:user_login')
class UserLogin(View):
    def get(self,request):
        form_instance=LoginForms()
        return render(request,'login.html',{'form':form_instance})
    def post(self,request):
        form_instance =LoginForms(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd)
            if user and user.is_superuser==True :
                login(request,user)
                return redirect('shop:admin_home')
            elif user and user.is_superuser != True:
                login(request, user)
                return redirect('shop:category')

            else:
                messages.error(request,"Invalid Credentails,Please enter valid Username and Password")
                return render(request, 'login.html',{'form': form_instance})
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop:category')
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
class AddCategory(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_fun(self):
        return self.request.user.is_superuser
    def get(self,request):
        form_instance=CategoryForm()
        return render(request,'addcategory.html',{'form':form_instance})
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:admin_home')
class AddProduct(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_fun(self):
        return self.request.user.is_superuser
    def get(self,request):
        form_instance=ProductForm()
        return render(request,'addproduct.html',{'form':form_instance})
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:admin_home')
class AddStock(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(instance=p)
        return render(request,'addstock.html',{'form':form_instance})
    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')

