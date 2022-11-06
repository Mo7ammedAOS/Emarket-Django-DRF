from django.contrib import admin
from order.models import  Payment, Order , Product_order
# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Product_order)