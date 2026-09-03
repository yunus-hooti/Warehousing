from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'amount', 'good_code']
    list_filter = ['category', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
