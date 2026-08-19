from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'middle_name', 'last_name', 'role')}),
        ('Access rights', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)