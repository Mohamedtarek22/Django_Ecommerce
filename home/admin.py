from django.contrib import admin
from home.models import Setting
from home.models import ContactMessage
# Register your models here.
class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']
admin.site.register(Setting,SettingtAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

admin.site.register(ContactMessage,ContactMessageAdmin)