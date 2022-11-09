from django.contrib import admin
from order.models import  Payment, Order , Product_order
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = Product_order
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'is_ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone_number', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at',]
    list_filter = ['status', 'is_ordered'] 
    search_fields = ['order_number', 'first_name', 'last_name', 'phone_number', 'email', 'city']
    list_per_page = 10
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product_order)