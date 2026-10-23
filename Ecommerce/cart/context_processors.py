from cart.models import Cart
def cart_menu(request):
    count=0
    u=request.user
    try:
        c=Cart.objects.filter(user=u)
        for i in c:
            count+=i.quantity
    except:
        pass
    return {'count':count}