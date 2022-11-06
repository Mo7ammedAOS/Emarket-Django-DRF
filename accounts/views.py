from django.shortcuts import HttpResponse, redirect, render
from accounts.forms import RegisterForm
from django.contrib import messages ,auth
from accounts.models import Account
from django.contrib.auth.decorators import login_required 

# Verfication emails:
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart_e.views import _cart_id
from cart_e.models import Cart , CartItem
import requests


# Create your views here.

def register(request):
    #  sending data from frontend using forms.
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = f'@{first_name}'
        
            # print(first_name , email, phone_number)
            

            # saving data upove in the database

            new_user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password,

            )

            new_user.phone_number = phone_number
            
            # saving new_user in the database

            new_user.save()

            # User Activation:
            currnet_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/verification_email.html',{
                'user': new_user,
                'domain': currnet_site,
                'uid': urlsafe_base64_encode(force_bytes(new_user.id)),
                'token':default_token_generator.make_token(new_user),
            })
            # email input:
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # passing submit messages
            messages.success(request,'We have sent to you verification email, please confirm your email')
            return redirect('accounts:register')

    else:
        form = RegisterForm()
    
    context = {
        'form':form
    }
    return render(request,'accounts/register.html',context)

# login functionality

def login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
            # print(email, password)
            # try:
            #     user = Account.objects.get(email = email, password = password)
            # except:
            #     HttpResponse('User not found')

        user = auth.authenticate(email = email, password = password)

        if user is not None:

            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_items_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_items_exists:
                    cartItems = CartItem.objects.filter(cart = cart)

                    # Getting product variations by id
                    product_variations = []

                    for item in cartItems:
                        ex_variations = item.variations.all()
                        product_variations.append(list(ex_variations))

                    # Get CartItem by using user and get It's product variations.
                    cartitems = CartItem.objects.filter(user = user)

                    existing_variations_list = []
                    id_s = []

                    for item in cartitems:
                        existing_variations = item.variations.all()
                        existing_variations_list.append(list(existing_variations))

                        id_s.append(item.id)
                    
                    for attribute in product_variations:
                        if attribute in existing_variations_list:
                            index = existing_variations_list.index(attribute)
                            item_id = id_s[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cartitems = CartItem.objects.filter(cart = cart)
                            for item in cartitems:
                                item.user = user
                                item.save()

                    # for item in cartItems:
                    #     item.user = user
                    #     item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                pms = dict(x.split('=') for x in query.split('&'))
                if 'next' in pms:
                    next_page = pms['next']
                    return redirect(next_page)
            except:   
                return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('accounts:login') 
        
    
    return render(request,'accounts/login.html')

@login_required(login_url='accounts:login')
def logout(request):

    auth.logout(request)
    messages.success(request,'You are logged out')

    
    return redirect('accounts:login')

def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation your account is activated')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:register')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email = email ).exists():
            user = Account.objects.get(email__exact = email)

            
            # User Activation:
            currnet_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': currnet_site,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user),
            })
            # email input:
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # passing submit messages
            messages.success(request,'Password reset email has been sent to your email address !')
            return redirect('accounts:login')

        else:
            messages.error(request,'Account does not exists')
            return redirect('accounts:forgot_password')
    return render(request,'accounts/forgotpassword.html')

def validated_password_reset(request,uidb64, token):
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password ')
        return redirect('accounts:reset_password')
    else:
        messages.erro(request,'This link has been expired')
        return redirect('accounts:login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmed_password = request.POST.get('confirmed_password')

        if password == confirmed_password:
            uid = request.session.get('uid')
            user= Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request,'New password has been set successfully')
            return redirect('accounts:login')

        else:
            messages.erro(request,'Passwords do not match!')
            return redirect('accounts:reset_password')
    else:
        return render(request,'accounts/reset_password.html')


def dashboard(request):
    return render(request,'accounts/dashboard.html')
