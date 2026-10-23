from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product")
    quantity=models.IntegerField(default=1)
    updated=models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.user.username
from django.utils import timezone
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    phno=models.IntegerField()
    amount=models.IntegerField(null=True)
    payment_method=models.CharField(max_length=50)
    order_id=models.CharField(null=True,max_length=70)
    ordered_date=models.DateTimeField(default=timezone.now())
    is_ordered=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.order_id)
class Order_details(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
