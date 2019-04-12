# Django admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Local imports
# Models
from .models import(
    CustomUser
)


class CustomUserAdmin(UserAdmin):
    # Set fields to be displayed on the users list page
    list_display = ['id', 'username', 'email', 'is_staff']


"""
Registered models
"""
admin.site.register(CustomUser, CustomUserAdmin)