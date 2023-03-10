from django.shortcuts import render,redirect
from Accounts.views import home
from user.models import User
from store.models import *
from category.models import *
from orders.models import*
from carts.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ProductForm,VariationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import IntegrityError



# Create your views here.
# count the all nos
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def admin_dashboard(request):
    user_count=User.objects.filter(is_superuser=False).count()
    product_count=Product.objects.all().count()
    order_count=OrderProduct.objects.filter(ordered=True).count()
    category_count=Category.objects.all().count()
    variation_count=Variation.objects.all().count()
    admin_order_count=User.objects.filter(is_superuser=True).count()

    context={
        'user_count':user_count,
        'product_count':product_count,
        'order_count':order_count,
        'category_count':category_count,
        'variation_count':variation_count,
        'admin_order_count':admin_order_count,

    }
    return render(request,'adminpanel/admin_dashboard.html',context)

# user_managment
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def user_managment(request):
    if 'key' in request.GET:
        key=request.GET['key']
        print(key)
        users=User.objects.order_by('-id').filter(Q(first_name__icontains=key)|Q(email__icontains=key))
    else:
        users=User.objects.filter(is_superuser=False).order_by('id')

    paginator = Paginator(users, 2)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context={
        # 'users':users,
        'users':paged_users,
    }
    return render(request,'adminpanel/user_managment.html',context)
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def user_ban(request,user_id):
    user=User.objects.get(id=user_id)
    user.is_active=False
    user.save()
    return redirect('user_managment')
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def user_unban(request,user_id):
    user=User.objects.get(id=user_id)
    user.is_active=True
    user.save()
    return redirect('user_managment')

#category_managment

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def category_management(request):
    if  request.method =='POST':
        keyword=request.POST['keyword']
        print(keyword)
        categories=Category.objects.order_by('id').filter(Q(category_name__startswith=keyword)|Q(slug__startswith=keyword))
    else:
      categories=Category.objects.all().order_by('id')
    paginator = Paginator(categories, 4)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    messagess = messages.get_messages(request)
    context={
        # 'categories':categories,
        'categories':paged_categories,
        'messages': messagess
    }
    return render(request,'adminpanel/category_management.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST['category_name']
            category_slug = request.POST['category_slug']
            category_description = request.POST['category_description']
            
            # Check if category name is empty or contains only whitespace characters
            if not category_name or not category_name.strip():
                messages.error(request, 'Category name cannot be empty.')
                return render(request, 'adminpanel/add_category.html')

            if Category.objects.filter(category_name__iexact=category_name.lower().replace(' ', '')).exists():
                messages.error(request, 'Category already exists.')
            else:
                categories = Category.objects.create(
                    category_name=category_name,
                    slug=category_slug,
                    desciption=category_description
                )
                messages.success(request, 'Category created successfully.')
                return redirect('category_management')
        except IntegrityError:
            messages.error(request, 'Category already exists.')
            return render(request, 'adminpanel/add_category.html')
    return render(request, 'adminpanel/add_category.html')


@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def update_category(request,category_id):
    try:
        categories=Category.objects.get(id=category_id)
        if request.method == 'POST':
            category_name=request.POST['category_name']
            category_slug=request.POST['category_slug']
            category_description=request.POST['category_description']
            categories.category_name=category_name
            categories.slug=category_slug
            categories.desciption=category_description
            categories.save()
            return redirect('category_management')
        context={
                  'category':categories,
                    } 
    except Exception as e:
        raise e
    
    return render(request,'adminpanel/update_category.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def delete_category(request,delete_id):
    categories=Category.objects.get(id=delete_id)
    categories.delete()
    return redirect('category_management')


################ product managment ###############
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def product_management(request):
    if request.method=='POST':
        key=request.POST['key']
        products=Product.objects.order_by('id').filter(Q(product_name__icontains=key))
    else:
      products=Product.objects.all().order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    context={
        # 'products':products
        'products':paged_categories
    }
    return render(request,'adminpanel/product_management.html',context)

#add product 
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'adminpanel/add_product.html', context)
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def edit_product(request,product_id):
    products=Product.objects.get(id=product_id)
    form=ProductForm(instance=products)
    if request.method == 'POST':
        try:
            form = ProductForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
               
                return redirect('product_management')
            

        except Exception as e:
            raise e

    context = {
        'product': products,
        'form': form
    }
    return render(request,'adminpanel/edit_product.html',context)
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def delete_product(request,delete_id):
    products=Product.objects.get(id=delete_id)
    products.delete()
    return redirect('product_management')

################################### Order  Managment #############################
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def order_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__contains=key) | Q(user__email__contains=key) | Q(first_name__icontains=key)).order_by('id')
    else:
        orders = Order.objects.filter(is_ordered=True).order_by('-id')

    paginator = Paginator(orders, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'orders': paged_orders
    }
    return render(request,'adminpanel/order_management.html', context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def accept_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Shipped'
    order.save()

    return redirect('order_management')

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def complete_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Delivered'
    order.save()

    return redirect('order_management')

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def manager_cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('order_management')

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('admin_orders')

######################## variation  management #####################
@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def variation_management(request):
    if request.method == 'POST':
        keyword=request.POST['keyword']
        variations=Variation.objects.filter(Q(product__product_name__icontains=keyword) | Q(variation_category__icontains=keyword) | Q(variation_values__icontains=keyword)).order_by('id')
    else:

        variations=Variation.objects.all().order_by('id')
    paginator = Paginator(variations, 4)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations': paged_variations
    }
    return render(request,'adminpanel/variation_management.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm()

    context = {
        'form': form
    }
    return render(request, 'adminpanel/add_variation.html', context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def update_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)

    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm(instance=variation)

    context = {
        'variation': variation,
        'form': form
    }
    return render(request, 'adminpanel/update_variation.html', context)

@user_passes_test(lambda u: u.is_superuser,login_url=home)
@login_required(login_url='login')
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    variation.delete()
    return redirect('variation_management')

# def admin_order(request):
#     if request.user.is_authenticated:

#         current_user = request.user
#         try:
#            if request.method == 'POST':
#             keyword = request.POST['keyword']
#             orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__contains=keyword) | Q(user__email__icontains=keyword) | Q(first_name__startswith=keyword) | Q(last_name__startswith=keyword) | Q(phone__startswith=keyword)).order_by('-created_at')
#            else:
#             orders = Order.objects.filter(
#                 user=current_user)
#         except Exception as e:
#            raise e
#            # add a return statement here
#            return HttpResponseBadRequest("Bad Request")
#         paginator = Paginator(orders, 10)
#         page = request.GET.get('page')
#         paged_orders = paginator.get_page(page)
#         context = {
#              'orders': paged_orders,
#         }
#         return render(request, 'admin_panel/admin_order.html', context)
