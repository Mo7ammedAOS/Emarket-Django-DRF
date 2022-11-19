from django.shortcuts import render
from store.models import Product, ReviewRate

# Create your views here.


def main(request):

    products = Product.objects.all().filter(is_available = True).order_by('-created')
    for product in products:
        reviews = ReviewRate.objects.filter(product_id = product.id , status = True)

    context = {
        'products':products,
        'reviews':reviews
    }
    return render(request,'main/home.html',context)

