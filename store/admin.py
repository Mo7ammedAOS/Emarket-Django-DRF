from django.contrib import admin
from .models import Product, Product_Gallery , Variation , ReviewRate
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class Product_Gallery_Inline(admin.TabularInline):
    model = Product_Gallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'updated', 'is_available']
    inlines = [Product_Gallery_Inline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active', 'created']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value', 'is_active', 'created']


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRate) 
admin.site.register(Product_Gallery)
