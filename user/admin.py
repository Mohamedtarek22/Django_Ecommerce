from django.contrib import admin
from order.models import Wishlist

# Register your models here.
from user.models import UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address', 'phone','city','country','status_address'
                    # 'language','currency','image_tag']
                    ]
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Wishlist)