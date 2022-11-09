
from django.shortcuts import render , HttpResponse , redirect  
from order.forms import OrderForm
from order.models import Order , Payment, Product_order
from cart_e.models import CartItem
import datetime
from django.http import JsonResponse
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json

# Create your views here.
# @csrf_protect
def payment(request):
    body = json.loads(request.body)
    
    
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    #  Store Fetched Data From online payment
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Passing cart items to product order:
    cartItems = CartItem.objects.filter(user = request.user)
    
    for item in cartItems:
        product_order = Product_order()
        product_order.order_id = order.id
        product_order.user_id = request.user.id
        product_order.product_id = item.product_id
        product_order.quantity = item.quantity
        product_order.product_price = item.product.price
        product_order.is_ordered = True
        product_order.payment = payment
        product_order.save()

        cartitems = CartItem.objects.get(id = item.id)
        product_variation = cartitems.variations.all()
        product_order = Product_order.objects.get(id = product_order.id)
        product_order.variation.set(product_variation)
        product_order.save()

        # reduce product's stock:
        product  = Product.objects.get(id =item.product_id)
        product.stock -= item.quantity
        product.save()

    #     # clear cart items:

    CartItem.objects.filter(user = request.user).delete()
    user = request.user

        # send email to user that his order has been placed:

    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_recieved_email.html',{
                'user': user,
                'order':order
            })
            # email input:
    to_email = item.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

        # Send order number and transID back to senDate function via JsonResponse:
    data={
            'order_number': order.order_number,
            'transID':payment.payment_id

        }

    return JsonResponse(data)



    return render(request,'orders/payment.html')

def place_order(request, total = 0, quantity = 0):
    
    
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
    taxs = (5 * total)* 0.01
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
            order_number = f'{current_date}{data.id}'
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user =current_user, order_number = order_number)
            context = {
                'order': order,
                'cartitems': cartItems,
                'total': total,
                'taxs': taxs,
                'grand_total': grand_total
            }
            return render(request,'orders/payment.html', context)
    else:
        print('not posted')
        return redirect('cart:checkout')

    
    # Order Complete:

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        product_ordered = Product_order.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id = transID)

        sub_total = 0

        for i in product_ordered:
            sub_total += i.product_price * i.quantity

        context = {
            'order':order,
            'product_ordered':product_ordered,
            'transID':payment.payment_id,
            'payment': payment,
            'sub_total':sub_total
        }
        return render(request,'orders/order_complete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):

        return redirect('home:main')
    
        




