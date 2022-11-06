from django.shortcuts import HttpResponse, render, redirect
from store.models import Product , Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

'''This function is to fetch or create a session key
for using it as cart id
'''
def _cart_id(request):

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = Product.objects.get(id = product_id)
        product_variation = []
        if request.method ==  'POST' :
            for item in request.POST:
                key = item
                value = request.POST.get(key)

                # print(key,value)
                
                try:
                    variation = Variation.objects.get(product = product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                    # print(variation)
                except:
                    pass

        # Briging product
        

        # return HttpResponse(product.product_name)

        # get or create cartby try and exception

        

        # placing product in cart by using cartitem

        is_cart_items_exist = CartItem.objects.filter(product = product,user = current_user).exists()
        if is_cart_items_exist:

            cartitems = CartItem.objects.filter(product = product, user = current_user)

            existing_variations_list = []
            id_s = []

            for item in cartitems:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))

                id_s.append(item.id)
            # print(existing_variations_list)

            if product_variation in existing_variations_list:
                # increment item.quantity + 1
                index = existing_variations_list.index(product_variation)
                item_id = id_s[index]
                item = CartItem.objects.get(id = item_id,product = product)
                item.quantity += 1
                item.save() 
            else:
                # create new caritem
                item = CartItem.objects.create(product = product, quantity = 1 , user = current_user)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    
                item.save()
        else:
            cartitems = CartItem.objects.create(
                product = product,
                user = current_user,
                quantity = 1

            )

            if len(product_variation)>0:
                cartitems.variations.clear()
                cartitems.variations.add(*product_variation)
            cartitems.save()

        return redirect('cart:cart')
    else:
        product = Product.objects.get(id = product_id)
        product_variation = []
        if request.method ==  'POST' :
            for item in request.POST:
                key = item
                value = request.POST.get(key)

                # print(key,value)
                
                try:
                    variation = Variation.objects.get(product = product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                    # print(variation)
                except:
                    pass

        # Briging product
        

        # return HttpResponse(product.product_name)

        # get or create cartby try and exception

        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))

            # return HttpResponse(cart.cart_id)

        except Cart.DoesNotExist:

            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        # placing product in cart by using cartitem

        is_cart_items_exist = CartItem.objects.filter(product = product,cart = cart).exists()
        if is_cart_items_exist:

            cartitems = CartItem.objects.filter(product = product, cart = cart)

            existing_variations_list = []
            id_s = []

            for item in cartitems:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))

                id_s.append(item.id)
            # print(existing_variations_list)

            if product_variation in existing_variations_list:
                # increment item.quantity + 1
                index = existing_variations_list.index(product_variation)
                item_id = id_s[index]
                item = CartItem.objects.get(id = item_id,product = product)
                item.quantity += 1
                item.save() 
            else:
                # create new caritem
                item = CartItem.objects.create(product = product, quantity = 1 , cart = cart)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    
                item.save()
        else:
            cartitems = CartItem.objects.create(
                product = product,
                cart = cart,
                quantity = 1

            )

            if len(product_variation)>0:
                cartitems.variations.clear()
                cartitems.variations.add(*product_variation)
            cartitems.save()

        return redirect('cart:cart')
        

def cart(request, total = 0 , quantity = 0 , cartItems = None):

    try:
        tax = 0
        assembled_total = 0
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user = request.user , is_active = True)
            print(request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cartItems = CartItem.objects.filter(cart = cart , is_active = True)
        for item in cartItems:
            total = total + (item.product.price * item.quantity)
            # calculating the total includes taxs:
            tax = (5 * total)/100   # 5 % for tax
            assembled_total = total + tax

            quantity = quantity + item.quantity

    except ObjectDoesNotExist:
        pass

    context ={
        'cartItems':cartItems,
        'total':total,
        'tax':tax,
        'assembled_total':assembled_total,
        'quantity':quantity
    }

    return render(request,'store/cart.html',context)


def decrement_cart(request,product_id, cartItem_id):

    product = Product.objects.get(id = product_id)
    try:
        if request.user.is_authenticated:
            cartitem = CartItem.objects.get(product = product , user = request.user ,id = cartItem_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cartitem = CartItem.objects.get(product = product , cart = cart ,id = cartItem_id)

        if cartitem.quantity > 1:

            cartitem.quantity -= 1

            cartitem.save()
        
        else:

            cartitem.delete()
    except:
        pass

    return redirect('cart:cart')

def remove_cart_item(request,product_id, cartItem_id):

    product = Product.objects.get(id = product_id)
    if request.user.is_authenticated:
        cartitem = CartItem.objects.get(product = product , user = request.user , id = cartItem_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cartitem = CartItem.objects.get(product = product , cart = cart , id = cartItem_id)

    cartitem.delete()

    return redirect('cart:cart')


# Checkout cartitems:

@login_required(login_url='accounts:login')
def checkout(request, total = 0 , quantity = 0 , cartItems = None):

    try:
        tax = 0
        assembled_total = 0
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user = request.user , is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cartItems = CartItem.objects.filter(cart = cart , is_active = True)
        for item in cartItems:
            total = total + (item.product.price * item.quantity)
            # calculating the total includes taxs:
            tax = (5 * total)/100   # 5 % for tax
            assembled_total = total + tax

            quantity = quantity + item.quantity

    except ObjectDoesNotExist:
        pass

    context ={
        'cartItems':cartItems,
        'total':total,
        'tax':tax,
        'assembled_total':assembled_total,
        'quantity':quantity
    }

    return render(request,'store/checkout.html',context)