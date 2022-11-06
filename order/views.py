from django.shortcuts import render , HttpResponse , redirect
from order.forms import OrderForm
from order.models import Order
from cart_e.models import CartItem
import datetime
from django.core.exceptions import BadRequest

# Create your views here.

def payment(request):
    return render(request,'orders/payment.html')

def place_order(request):
    total = 0 
    quantity = 0
    current_user = request.user

    cartItems = CartItem.objects.filter(user = current_user)
    ctItems_count = cartItems.count()
    if ctItems_count <= 0:
        return redirect('store:store')
    
    grand_total = 0
    taxs = 0
    for item in cartItems:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    taxs = (2 * total)* 0.01
    grand_total = total + taxs

    # Store billing information:
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = taxs
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            # Generate order number :
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            data.order_number = f'{current_date}{data.id}'
            data.save()
            return redirect('cart:checkout')
    else:
        print('not posted')
        return redirect('cart:checkout')
    
        




