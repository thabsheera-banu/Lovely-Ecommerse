from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from django.db.models import Q
from carts.views import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from carts.models import wishlist
from django.http.response import JsonResponse
from django.db.models import Max, Min


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None


    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Product_count = products.count()
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        # products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Product_count= products.count()

    maxx_price = Product.objects.aggregate(Max('price'))['price__max']
    minn_price = Product.objects.aggregate(Min('price'))['price__min']

    context = {
        'products': paged_products,
        # 'products':products,
        'MAX_price': maxx_price, 
        'MIN_price': minn_price,
        'Product_count': Product_count,

    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
     single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
     in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'in_cart':in_cart
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
             products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
             product_count = products.count()
    context = {
        'products': products,
        'Product_count': product_count,
    }
    return render(request, 'store/store.html',context)

def filter_by_price(request):
    
    min_price = float(request.GET.get('min_price').replace('$', ''))
    max_price = float(request.GET.get('max_price').replace('$', ''))
    
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    sizes = Product.objects.filter()
    context = {
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
        
        
    }
    return render(request, 'store/store.html', context)

