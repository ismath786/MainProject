from itertools import product

from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
from shop.models import Product
from cart.models import Cart,Order_details,Order
from cart.forms import OrderForm
import razorpay
from django.contrib import messages
# Create your views here.
class AddToCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cart_view')
class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        return render(request,'cart.html',{'cart':c,'total':total})
class CartDecrement(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(product=p,user=u)
            if c.quantity>1:
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cart_view')
class CartRemove(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.delete()
        except:
            pass
        return redirect('cart:cart_view')
def check_stock(c):
    stock=True
    for i in c:
        if i.product.stock < i.quantity:
            stock=False
            break
    return stock
class Check_Out(View):
    def get(self,request):
        form_instance=OrderForm()
        c=Cart.objects.all()
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        return render(request,'checkout.html',{'form':form_instance,'cart':c,'total':total})
    def post(self,request):
        u = request.user
        c = Cart.objects.filter(user=u)
        stock=check_stock(c)
        if stock:
            form_instance=OrderForm(request.POST)
            print(request.POST)
            if form_instance.is_valid():
                o=form_instance.save(commit=False)

                o.user=u
                o.save()

                total=0
                for i in c:
                    total+=i.product.price*i.quantity
                    order=Order_details.objects.create(order=o,product=i.product,quantity=i.quantity)
                    order.save()
                if o.payment_method=='Online':
                    client=razorpay.Client(auth=('rzp_test_TpgiNijpsOtfUF','Stit68KRV5oO4sYS8dsXeyQu'))
                    response_payment = client.order.create(dict(amount=total * 100, currency="INR"))
                    print(response_payment)
                    o.order_id=response_payment['id']
                    o.amount=total
                    o.save()
                    return render(request,'payment.html',{'payment':response_payment})
                elif o.payment_method=='COD':
                    o.is_ordered=True
                    o.amount=total
                    o.save()
                    items=Order_details.objects.filter(order=o)
                    for i in items:
                        i.product.stock-=i.quantity
                        i.product.save()
                        c.delete()
                    return redirect('shop:category')
                else:
                    pass
                return redirect('shop:category')

        else:
            messages.error(request,"Sorry Currenty Items not available,Try again later")
            return render(request,'payment.html')
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
class Payment(View):
    def get(self,request):
        return render(request,'payment.html')
@method_decorator(csrf_exempt,name="dispatch")
class Payment_Success(View):
    def post(self,request,i):
        u=User.objects.get(username=i)
        login(request,u)
        print(request.POST)
        id=request.POST['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()
        items=Order_details.objects.filter(order=o)
        for i in items:
            i.product.stock-=i.quantity
            i.product.save()
        c=Cart.objects.filter(user=u)
        c.delete()
        return render(request,'payment_success.html')
class YourOrder(View):
    def get(self,request):
        u=request.user
        o_items=Order.objects.filter(user=u,is_ordered=True)
        return render(request,'order.html',{'oders':o_items})




