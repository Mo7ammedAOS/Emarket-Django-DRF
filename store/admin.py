from django.contrib import admin
from .models import Product , Variation , ReviewRate

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'updated', 'is_available']

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active', 'created']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value', 'is_active', 'created']

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRate)

