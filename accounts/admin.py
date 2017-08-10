# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import (
    GroupAdmin,
    UserAdmin as BaseUserAdmin,
)
from django.contrib.auth.models import Group
from .forms import (
    AdminUserChangeForm,
    UserCreationForm,
)
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


def deactivate_users(modeladmin, news, queryset):
    queryset.update(is_active=False)
deactivate_users.short_description = "Deactivate selected users"


class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = UserCreationForm
    list_display = ['username', 'email', 'first_name', 'last_name', 'client', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = list_display
    list_filter = ['last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'client', 'password')}),
        (_('Permissions'), {'fields': ('is_active','is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'email', 'first_name', 'last_name', 'client', 'password1', 'password2')}
        ),
    )
    search_fields = ['username', 'client', 'email', 'first_name', 'last_name']
    actions = [deactivate_users]
    ordering = ['username']
    filter_horizontal = ()


class UserGroupInline(admin.TabularInline):
    model = User.groups.through
    extra = 0


class MyGroupAdmin(GroupAdmin):
    search_fields = ['name']
    inlines = [UserGroupInline]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
