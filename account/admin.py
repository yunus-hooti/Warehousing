from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CreationForm,ChangeForm
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username','phon','email']
    ordering = ('username',)
    add_form = CreationForm
    form = ChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','email')}),
        ('Permissions', {'fields': ('supplier_user','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1','password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name','email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )