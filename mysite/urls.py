"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import ContextManager
from django.contrib import admin, auth
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from home import views
from order import views as OrderViews
from product.models import Category
from user import views as UserViews
from product import views as ProductViews
urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('user/', include('user.urls')),
    path('jet/',include('jet.urls')),
    path('jet/dashboard',include('jet.dashboard.urls','jet-dashboard')),
    path('admin/', admin.site.urls),
    path('',include('home.urls')) , 
    path('home/',include('home.urls')),
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('search/',views.search,name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('login/', UserViews.login_form, name='login_form'),
    path('logout/', UserViews.logout_form, name='logout_form'),
    path('filter-data',views.filter_data,name="filter_data"),
    path('signup/', UserViews.signup_form, name='signup_form'),
    path('add-to-cart', OrderViews.add_to_cart, name='add_to_cart'),
    path('cart', OrderViews.cart_list, name='cart'),
    path('delete-from-cart', OrderViews.delete_cart_item, name='delete_cart_item'),
    path('update-cart', OrderViews.update_cart_item, name='update_cart'),
    path('checkout', OrderViews.checkout, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', OrderViews.payment_done, name='payment_done'),
    path('payment-cancelled/', OrderViews.payment_canceled, name='payment_cancelled'),
    path('my-dashboard', UserViews.my_dashboard, name='my_dashboard'),
    path('my-orders', UserViews.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>', UserViews.my_orders_items, name='my_orders_items'),
    path('add-wishlist', UserViews.add_wishlist, name='add_wishlist'),
    path('my-wishlist', UserViews.my_wishlist, name='my_wishlist'),
    path('my-addressbook', UserViews.my_addressbook, name='my_addressbook'),
    path('add-address', UserViews.save_address, name='add-address'),
    path('activate-address', UserViews.activate_address, name='activate-address'),
    path('edit-profile', UserViews.edit_profile, name='edit-profile'),
    path('update-address<int:id>', UserViews.update_address, name='update-address'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html',
    extra_context={'category':Category.objects.all()}

    ),name='password'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html',
    extra_context={'category':Category.objects.all()}

    ),name='password'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html',
    extra_context={'category':Category.objects.all()}

    ),name='password_change_done'),

    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',
    extra_context={'category':Category.objects.all()}

    ),name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html',
    extra_context={'category':Category.objects.all()}

    ),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',  auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
    extra_context={'category':Category.objects.all()}

    ),name='password_reset_confirm'),

    path('reset/done/',  auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complate.html',
    extra_context={'category':Category.objects.all()}

    ),name='password_reset_complete'),


    
   

    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #  name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)