from django.urls import path
from . import views

# app name: 
app_name = 'accounts'

urlpatterns = [
    path('register/' ,views.register, name='register'),
    path('login/' ,views.login, name='login'),
    path('logout/' ,views.logout, name='logout'),
    path('forgot_password/' ,views.forgotpassword, name='forgot_password'),
    path('change_password/' ,views.change_password, name='change_password'),
    path('dashboard/' ,views.dashboard, name='dashboard'),
    path('user_orders/' ,views.user_orders, name='user_orders'),
    path('user_orders_details/<int:od_id>/' ,views.user_orders_details, name='user_orders_details'),
    path('edit_profile/' ,views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/' ,views.activate, name='activate'),
    path('validated_password_reset/<uidb64>/<token>/' ,views.validated_password_reset, name='validated_password_reset'),
    path('reset_password/',views.reset_password, name='reset_password'),  
]
