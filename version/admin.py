# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Change,
    Client,
    File,
    Loggs,
    Version,
)


class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'ein', 'sec_level', 'license_date', 'city', 'zipcode', 'street', 'phone_number']
    list_display_links = list_display
    list_filter = ['city', 'sec_level']
    search_fields = list_display


class ChangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'sec_level', 'change_type', 'version', 'client', 'description']
    list_display_links = list_display
    list_filter = ['date', 'change_type', 'sec_level', 'client']
    search_fields = list_display

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChangeAdmin, self).get_form(request, obj, **kwargs)
        try:
            form.base_fields['version'].initial = Change.objects.first().version
        except:
            pass
        return form


class FileAdmin(admin.ModelAdmin):
    list_display = ['version', 'filename', 'file']
    search_fields = ['filename', 'file']
    list_filter = ['version']


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class VersionAdmin(admin.ModelAdmin):
    list_display = ['version', 'version_date', 'description']
    list_display_links = list_display
    list_filter = ['version_date']
    search_fields = ['version', 'version_date', 'description']
    filter_horizontal = ['clients']
    inlines = [FileInline]


class LoggsAdmin(admin.ModelAdmin):
    list_display = ['logg_date', 'user', 'db_table', 'record_id']
    list_display_links = list_display
    search_fields = ['user__username', 'db_table']
    list_filter = ['logg_date', 'db_table']


admin.site.register(Client, ClientAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Loggs, LoggsAdmin)