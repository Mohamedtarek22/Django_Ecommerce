
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.contrib import messages

# Create your views here.
from product.models import Comment, CommentForm, Product, Category


def index(request):
    products =Product.objects.all()
    category= Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]

    context ={'products':products,'category':category,'products_slider':products_slider}
    return render(request,'category_products.html',context)



def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)