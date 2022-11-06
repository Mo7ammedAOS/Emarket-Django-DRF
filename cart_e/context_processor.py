from .models import Cart, CartItem
from .views import _cart_id

def cart_Items_counter(request):
    
    if 'admin' in request.path:
        return {}
    else:
        count_item = 0
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                
                cartItems = CartItem.objects.all().filter(user = request.user)
                
                
            else:
                cartItems = CartItem.objects.all().filter(cart = cart[:1])
            
            
            # print(cartItems.user)
            for item in cartItems:
                count_item += item.quantity
        except Cart.DoesNotExist:
            count_item = 0
            
    return dict(count_item  = count_item)