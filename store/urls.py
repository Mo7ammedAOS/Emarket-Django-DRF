from django.urls import path
from . import views



app_name = 'store'


urlpatterns = [
    path('store',views.store, name = 'store'),
    path('category/<slug:catg_slug>/',views.store, name = 'productByCatg'),
    path('<slug:catg_slug>/<slug:product_slug>/',views.product_detail, name = 'product_detail'),
    path('search/',views.search, name = 'search'),

]