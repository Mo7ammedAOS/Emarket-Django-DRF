from sre_constants import CATEGORY
from sre_parse import CATEGORIES
from unicodedata import category
from django.shortcuts import HttpResponse, render, get_object_or_404
from category.models import Category
from store.models import Product
from cart_e.models import CartItem,Cart
from cart_e.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



# Create your views here.

def store(request, catg_slug = None):
    categories = None
    products    = None

    if catg_slug != None:
        categories = get_object_or_404(Category,slug = catg_slug)
        products   = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products    = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count() 

    context     = {
        'products':paged_products,
        'product_count':product_count
    }
    return render(request,'store/store.html', context)


def product_detail(request, catg_slug, product_slug):
    try:
        product_information = Product.objects.get(category__slug = catg_slug, slug = product_slug)
        is_it_Incart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = product_information).exists()
    except:
        raise HttpResponse("no such product")

    context = {'product_information':product_information,'is_it_Incart':is_it_Incart}
    return render(request,'store/product_detail.html',context)


def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')

        products = Product.objects.filter(
            Q(description__icontains = keyword)|
            Q(product_name__icontains = keyword)
        )
        product_count = products.count()

    return render(request,'store/store.html',{'products':products,'product_count':product_count})