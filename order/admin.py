from django.contrib import admin

# Register your models here.
from order.models import CartOrder, CartOrderItems, ShopCart, Order, OrderProduct, Wishlist


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user',
                    'quantity','price','amount'
                    ]
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip', 'last_name','phone','city','total')
    can_delete = False
    # inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount']
    list_filter = ['user']

# admin.site.register(ShopCart,ShopCartAdmin)
# admin.site.register(Order,OrderAdmin)
# admin.site.register(OrderProduct,OrderProductAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    list_editable=['paid_status','order_status']
    list_display = ['user', 'total_amt','paid_status','order_dt','order_status']

admin.site.register(CartOrder,CartOrderAdmin)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no','item','image_tag','qty','price','total']

admin.site.register(CartOrderItems,CartOrderItemsAdmin)

