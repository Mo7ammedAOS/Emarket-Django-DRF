from django.shortcuts import render
from store.models import Product
from cart_e.views import cart
# Create your views here.


def main(request):

    products = Product.objects.all().filter(is_available = True)

    context = {
        'products':products
    }
    return render(request,'main/home.html',context)

