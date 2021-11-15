from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from order.models import CartOrder, CartOrderItems, Wishlist
# Create your views here.
from product.models import Category, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.forms import AddressBookForm, ProfileForm, SignUpForm
from user.models import UserProfile
from django.template.loader import render_to_string
from django.db.models.functions import ExtractMonth
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Max,Min,Count,Avg
@login_required(login_url='/login') # Check login
def index(request):
    category=Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.filter(user_id=current_user.id)
    context = { 'category': category,
        'profile': profile}
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.filter(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url
            #{{request.session.userimage}}
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context ={'category':category}
    return render(request, 'login_form.html',context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            # data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/add-address')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Category.objects.all()
    context = { 'category': category,
        'form': form,
    }

    return render(request, 'signup_form.html',context)


def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)
import calendar
def my_dashboard(request):
    category = Category.objects.all()
    orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber=[]
    totalOrders=[]
    for d in orders:
	    monthNumber.append(calendar.month_name[d['month']])
	    totalOrders.append(d['count'])
    context = {
            'category': category,
            'orders':orders,
            'monthNumber':monthNumber,
            'totalOrders':totalOrders
            
        }
    return render(request,'dashboard.html',context)

def my_orders(request):
    category = Category.objects.all()
    orders=CartOrder.objects.filter(user=request.user)
    context = {
            'category': category,
            'orders':orders
            
        }
    return render(request,'orders.html',context)

def my_orders_items(request,id):
    category = Category.objects.all()
    order=CartOrder.objects.get(pk=id)

    orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
    context = {
            'category': category,
            'order':order,
            'orderitems':orderitems
            
        }
    return render(request,'order-items.html',context)
def add_wishlist(request):
    category = Category.objects.all()
    pid=request.GET['product']
    product=Product.objects.get(pk=pid)
    data={}
    checkw=Wishlist.objects.filter(product=product,user=request.user).count()
    if checkw > 0:
        data={
            'bool':False
        }
    else:
        wishlist=Wishlist.objects.create(
        product=product,
        user=request.user,
        )
        data={
            'bool':True
        }

    return JsonResponse(data)

def my_wishlist(request):
    category = Category.objects.all()
    wlist=Wishlist.objects.filter(user=request.user)
    context = {
            'category': category,
            'wlist':wlist
            
        }
    return render(request,'wishlist.html',context)

def my_addressbook(request):
    category = Category.objects.all()
    addbook=UserProfile.objects.filter(user=request.user)
    context = {
            'category': category,
            'addbook':addbook
            
        }
    return render(request,'addressbook.html',context)

def save_address(request):
    msg=None
    category = Category.objects.all()
    if request.method=='POST':
        form=AddressBookForm(request.POST)
        if form.is_valid():
            saveForm =form.save(commit=False)
            saveForm.user=request.user
            if 'status_address' in request.POST:
                UserProfile.objects.update(status_address=False)
            saveForm.save()
            msg='Data has been saved'


    form=AddressBookForm
    context = {
            'category': category,
            'form':form,
            'msg':msg
        }
    return render(request,'add-address.html',context)
def activate_address(request):
    a_id=request.GET['id']
    UserProfile.objects.update(status_address=False)
    UserProfile.objects.filter(id=a_id).update(status_address=True)
    # data={'bool'}
    return JsonResponse({'bool':True})

def edit_profile(request):
    msg=None
    if request.method=='POST':
        form=ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg='Data has been saved'
    form=ProfileForm(instance=request.user)
    category = Category.objects.all()

    context={
            'category': category,
            'msg':msg
            ,'form':form
    }
    return render(request,'edit-profile.html',context)

def update_address(request,id):
    address=UserProfile.objects.get(pk=id)
    msg=None
    category = Category.objects.all()
    if request.method=='POST':
        form=AddressBookForm(request.POST,instance=address)
        if form.is_valid():
            saveForm =form.save(commit=False)
            saveForm.user=request.user
            if 'status_address' in request.POST:
                UserProfile.objects.update(status_address=False)
            saveForm.save()
            msg='Data has been saved'


    form=AddressBookForm(instance=address)
    context = {
            'category': category,
            'form':form,
            'msg':msg
        }
    return render(request,'update-address.html',context)