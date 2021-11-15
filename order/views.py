from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from order.models import CartOrder, CartOrderItems, ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product
from user.models import UserProfile
from paypal.standard.forms import PayPalPaymentsForm

def index(request):
    return HttpResponse("Order Page")
@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(product_id=id,user_id=current_user.id)  # Check product in shopcart
    if checkproduct:
            control = 1  # The product is in the cart
    else:
            control = 0  # The product is not in the cart"""


    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)
    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id,user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            # data.variant_id = None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    products_slider=Product.objects.all().order_by('id')[:4]
    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             'products_slider':products_slider,
             }
    return render(request,'shopcart_products.html',context)

@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")

def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile=UserProfile.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()  #
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'profile': profile,

               }
    return render(request, 'Order_Form.html', context)


def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
def cart_list(request):
    category = Category.objects.all()
    products_slider=Product.objects.all().order_by('id')[:4]
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])


    context={
             'category':category,
             'products_slider':products_slider,
             'cart_data':request.session['cartdata'],
             'totalitems':len(request.session['cartdata'])
             ,'total_amt':total_amt
             }
    return render(request,'shopcart_products.html',context)
def delete_cart_item(request):
    p_id=request.GET['id']
    if 'cartdata' in request.session:
	    if p_id in request.session['cartdata']:
		    cart_data=request.session['cartdata']
		    del request.session['cartdata'][p_id]
		    request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])

    t=render_to_string('ajax/shopcart_products.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/shopcart_products.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
@login_required(login_url='/login') # Check login
def checkout(request):
    total_amt=0
    totalAmt=0
    if 'cartdata'in request.session:
        for p_id,item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*float(item['price'])
    #process
    # Process Payment
    # order_id='123'
    #order
    order =CartOrder.objects.create(
        user=request.user,
        total_amt=totalAmt,


    )
    #end
    category = Category.objects.all()
    products_slider=Product.objects.all().order_by('id')[:4]
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
        #orderitem
        items=CartOrderItems.objects.create(
            order=order,
            invoice_no='INV-'+str(order.id),
            item=item['title'],
            image=item['image'],
            qty=item['qty'],
            price=item['price'],
            total=float(item['qty'])*float(item['price'])


        )
    host = request.get_host()
    paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		'amount': total_amt,
		'item_name': 'OrderNo-'+str(order.id),
		'invoice': 'INV-'+str(order.id),
		'currency_code': 'EGP',
		'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
		'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
    form = PayPalPaymentsForm(initial=paypal_dict)

    context={
             'category':category,
             'products_slider':products_slider,
             'cart_data':request.session['cartdata'],
             'totalitems':len(request.session['cartdata'])
             ,'total_amt':total_amt
             ,'form':form
             }
    
    return render(request,'Order_Form.html',context)

@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')
