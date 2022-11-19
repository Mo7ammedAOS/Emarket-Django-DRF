from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , UserProfile
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display       = ('email', 'first_name', 'last_name', 'username', 'joined_at', 'last_login_at', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields    = ('joined_at', 'last_login_at')
    ordering           = ('-joined_at',)
    
    filter_horizontal  = ()
    list_filter        = ()
    
class User_ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width ="30" style ="border-radius:50%;">'.format(object.profile_image.url))
    thumbnail.short_description = 'Profile Picture'
    list_display       = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, User_ProfileAdmin)


