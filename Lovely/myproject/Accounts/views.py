from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from orders.models import Order,OrderProduct
from .forms import UserForm,UserProfileForm
from .models import UserProfile
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)
    hot_trend = Product.objects.all().filter(hot_trend=True)
    facewash=Product.objects.filter(category__category_name='Foundation')
    foundation_count=facewash.count()
    lipstick_count = Product.objects.filter(category__category_name='Lipstick').aggregate(count=Count('id'))['count']
    facewash_count = Product.objects.filter(category__category_name='Facewash').aggregate(count=Count('id'))['count']


    context = {
        'products': products,
        'foundation_count':foundation_count,
        'lipstick_count':lipstick_count,
        'facewash_count':facewash_count,
        'hot_trend':hot_trend,
       
    }

    return render(request,'index.html',context)

def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user=request.user.id,is_ordered=True)
    orders_count = orders.count()
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        user_profile = None
    context={
        'orders_count':orders_count,
        'user_profile':user_profile
    }
    return render(request,'user/dashboard.html',context)


def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders
    }
    return render(request,'user/my_order.html',context)

def cancel_order_user(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order.status = 'Cancelled'
        order.save()

        return redirect('my_orders')
        
    except Exception as e:
        raise e
def complete_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Delivered'
    order.save()

    return redirect('my_orders')


def edit_profile(request):
    if UserProfile.objects.filter(user=request.user):
        userprofile = get_object_or_404(UserProfile, user=request.user)
        print("yes")
    else:
        userprofile = UserProfile.objects.create(user=request.user)
        print("no")

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': user_profile_form,
        'userprofile': userprofile
    }

    return render(request, 'user/edit_profile.html', context)

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'user/order_detail.html', context)

def contact(request):
    return render(request,'contact.html')
