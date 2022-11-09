from django.urls import path
from . import views



app_name = 'order'


urlpatterns = [
    path('place-order/',views.place_order, name = 'place_order'),
    path('payment/',views.payment, name = 'payment'),
    path('order_complete/',views.order_complete, name = 'order_complete'), 
]