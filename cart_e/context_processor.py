from .models import Cart, CartItem
from .views import _cart_id

def cart_Items_counter(request):
    counter = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cartItems = CartItem.objects.all().filter(cart = cart[:1])

            for item in cartItems:
                counter += item.quantity
        except Cart.DoesNotExist:
            counter = 0
    return dict(counter = counter)