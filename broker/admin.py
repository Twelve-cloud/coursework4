from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'category',
                ),
            },
        ),
    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'company',
    )
    fields = ('name', 'price', 'company')
    search_fields = ('name', 'price', 'company_name')


class RequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'company', 'price', 'type')
    search_fields = ('username', 'company')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Stock)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Request, RequestAdmin)

admin.site.site_header = 'Администрирование сайта'
admin.site.site_title = 'Администрирование'
admin.site.index_title = ''
