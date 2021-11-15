import json

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib import messages

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage
from order.models import ShopCart
from product.models import Category, Product, Images, Comment
from django.template.loader import render_to_string

def index(request):
    setting= Setting.objects.get(pk=1)
    category=Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:6]
    products_latest = Product.objects.all().order_by('-id')[:6] #last
    products_picked = Product.objects.all().order_by('?')[:6] #random
    images =Images.objects.all()
    products=Product.objects.all()
    page="home"
    context ={'setting':setting,'page':page,'category':category,'products':products,'products_slider': products_slider,'products_latest': products_latest,'products_picked': products_picked,'images':images}
    return render(request,'index.html',context)

def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count
# def shopcartcount2():
#     count = ShopCart.objects.all().count()
#     return count

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category=Category.objects.all()

    context = {'setting': setting,'category':category}
    return render(request, 'about.html', context)

def contactus(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category=Category.objects.all()

    form =ContactForm
    context = {'setting': setting,'form':form,'category':category}
    return render(request, 'contact.html', context)

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            products = Product.objects.filter(title__icontains=query)

            category = Category.objects.all()
            products_slider = Product.objects.all().order_by('id')[:4]
            context = {'products': products, 'query':query,
                       'category': category,'products_slider':products_slider }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def category_products(request,id,slug):
    # products = Product.objects.all()
    data = Product.objects.filter(category_id=id)
    # products2=Product.objects.all()
    category=Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    context ={'category':category,'data': data,'products_slider':products_slider}

    return render(request,'category_products.html',context)

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    products_slider = Product.objects.all().order_by('id')[:4]  
    comments= Comment.objects.filter(product_id=id,status='True')
    context = {'product': product, 'category': category,
               'images': images,'comments': comments,
               'products_slider':products_slider
               }
    return render(request, 'product_detail.html', context)


def filter_data(request):
    colors=request.GET.getlist('color[]')
    sizes=request.GET.getlist('size[]')
    allProducts=Product.objects.all().distinct()
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=allProducts.filter(price__gte=minPrice)
    allProducts=allProducts.filter(price__lte=maxPrice)


    if len(colors)>0:
        allProducts=allProducts.filter(color__id__in=colors).distinct().order_by('id')
    if len(sizes)>0:
	    allProducts=allProducts.filter(size__id__in=sizes).distinct().order_by('id')
    t= render_to_string('ajax/category_products.html',{'data':allProducts})
    return JsonResponse({'data':t})