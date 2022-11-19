from sre_constants import CATEGORY
from sre_parse import CATEGORIES
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import  redirect, render, get_object_or_404
from accounts.models import UserProfile
from category.models import Category
from store.models import Product, Product_Gallery
from cart_e.models import CartItem,Cart
from cart_e.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from store.models import ReviewRate
from store.form import ReviewForm
from order.models import Product_order
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def store(request, catg_slug = None):
    categories = None
    products    = None

    if catg_slug != None:
        categories = get_object_or_404(Category,slug = catg_slug)
        products   = Product.objects.all().filter(category = categories, is_available = True).order_by('-created')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products    = Product.objects.all().filter(is_available = True).order_by('-created')
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
        
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            any_order_there = Product_order.objects.filter(user = request.user , product_id = product_information.id).exists()
        except Product_order.DoesNotExist:
            any_order_there = None
    else:
        any_order_there = None
    
    
    reviews = ReviewRate.objects.filter(product_id = product_information.id , status = True)
   
    product_gallery = Product_Gallery.objects.filter(product_id = product_information.id)
    context = {
        'product_information':product_information,
        'is_it_Incart':is_it_Incart,
        'any_orders_there':any_order_there,
        'reviews':reviews,
        'product_gallery':product_gallery,
        }
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


def submited_reviews(request,prt_ID):
    
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRate.objects.get(user__id=request.user.id, product__id= prt_ID)
            form = ReviewForm(request.POST , instance=reviews)
            form.save()
            messages.success(request,'Thank you ! Your review has been updated')
            return redirect(url)

        except ReviewRate.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                info = ReviewRate()
                info.subject = form.cleaned_data['subject']
                info.rating = form.cleaned_data['rating']
                info.review = form.cleaned_data['review']
                info.ip =  request.META.get('REMOTE_ADDR')
                info.product_id= prt_ID
                info.user_id = request.user.id
                info.save()
                messages.success(request,'Thank you ! Your review has been submited')
                return redirect(url)
                
