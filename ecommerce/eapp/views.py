from multiprocessing import context
from re import U
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Catagories, Products
from .forms import *
import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def Home(request, *args, **kwargs):
    shoes_catagory = Catagories.objects.get(name = 'shoes')
    shoes = shoes_catagory.products_set.all()[:4]
    shirts_catagory = Catagories.objects.get(name = 'shirt')
    shirts = shirts_catagory.products_set.all()[:4]
    pants_catagory = Catagories.objects.get(name = 'pants')
    pants = pants_catagory.products_set.all()[:4]
    # if request.user.is_authenticated:
    #     cartItems = Order.get_cart_items
    # else:
    #     cartItems=0

    context={
        'shoes':shoes,
        'shirts':shirts,
        'pants':pants,
        # 'cartitems':cartItems
    }

    return render(request,'home.html',context) 

def about_us(request, *args, **kwargs):
    return render(request,'about.html')

def Customer_register(request, *args, **kwargs): 
    form = CustomerRegisterForm()
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            messages.success(request,f'Account successfully created for {username}: Login now')
            return redirect('login')
            
        else:
            form = CustomerRegisterForm()
    context = {'form': form}
    return render(request,'register.html',context)

def all(request,cata):
    catagory = Catagories.objects.get(name=cata)
    all = catagory.products_set.all()
    context={
        'all':all,
    }
    return render(request,'all.html',context) 

@login_required
def detail(request,product_id):
    product = Products.objects.get(id=product_id)
    context={
        'product':product,
    }
    print(context)
    return render(request,'detail.html',context)

@login_required
def profile(request, *args, **kwargs):
    return render(request,'profile.html')
    
@login_required
def update_profile(request, *args, **kwargs):
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()
    if request.method == 'POST':
        u_form =UserUpdateForm (request.POST,instance=request.user)
        p_form =ProfileUpdateForm (request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Account Update Successfully')
            return redirect('profile')
    else:
        u_form =UserUpdateForm (instance=request.user) 
        p_form =ProfileUpdateForm (request.FILES,instance=request.user.profile) 
    context = {
    'u_form':u_form,
    'p_form':p_form,
    }
    return render (request, 'profile_update.html',context)
@login_required
def cart(request, *args, **kwargs):
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,compelete=False)
        items =order.orderitem_set.all()
        
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,'cart.html',context)
@login_required 
def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action = data['action']

    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order ,created =Order.objects.get_or_create(customer=customer, compelete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    else:
        orderItem.quantity = (orderItem.quantity + 1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('it was added',safe=False)