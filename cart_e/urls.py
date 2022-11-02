from django.urls import path
from . import views

# app name: 
app_name = 'cart_e'

urlpatterns = [
    path('' ,views.cart ,name='cart'),
    path('add_cart/<int:product_id>/' ,views.add_cart ,name='add_cart'),
    path('decrement/<int:product_id>/<int:cartItem_id>/' ,views.decrement_cart ,name='decrement_cart'),
    path('remove_cart_item/<int:product_id>/<int:cartItem_id>/' ,views.remove_cart_item ,name='remove_cart_item'),

]