from django.contrib import admin
from django.contrib.admin.decorators import display
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'is_active',
        'is_verified',
        'is_staff',
        'data_joined',
        'last_login',
    ]

admin.site.register(User,UserAdmin)