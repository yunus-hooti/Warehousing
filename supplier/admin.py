from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name','created_at','is_active']
    list_filter = ['is_active',]


@admin.register(GoodSupplier)
class GoodSupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier','number','created_at']

    def get_good_list(self,obj):
        return ', '.join([i.name for i in obj.good.all()])

