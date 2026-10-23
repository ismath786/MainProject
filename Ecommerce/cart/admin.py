from django.contrib import admin
from cart.models import Cart

from cart.models import Order_details,Order

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_details)