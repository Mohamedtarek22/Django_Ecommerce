from django.contrib import admin

# Register your models here.
from order.models import ShopCart
from product.models import Brand, Category, Color, Product, Images,Comment, Size
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status']
    list_filter =['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count','title')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'image_tag','status']
    list_editable=['status']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)
# admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')


admin.site.register(Comment,CommentAdmin)

