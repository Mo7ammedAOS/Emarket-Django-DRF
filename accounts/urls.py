from django.urls import path
from . import views

# app name: 
app_name = 'accounts'

urlpatterns = [
    path('register/' ,views.register, name='register'),
    path('login/' ,views.login, name='login'),
    path('logout/' ,views.logout, name='logout'),
    path('forgot_password/' ,views.forgotpassword, name='forgot_password'),
    path('dashboard/' ,views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/' ,views.activate, name='activate'),
    path('validated_password_reset/<uidb64>/<token>/' ,views.validated_password_reset, name='validated_password_reset'),
    path('reset_password/',views.reset_password, name='reset_password'),
    
]