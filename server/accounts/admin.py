# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ('login',)
    list_display = ('login', 'name', 'surname', 'is_admin')
    search_fields = ('login', 'name', 'surname')
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Informacje osobiste', {'fields': ('name', 'surname')}),
        ('Uprawnienia', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'name', 'surname', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
