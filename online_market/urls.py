from django.urls import path
from . import views

# app name: 
app_name = 'online_market'

urlpatterns = [
    path('' ,views.main ,name='main'),
    
]