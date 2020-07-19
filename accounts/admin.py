from django.contrib import admin
from .models import User, Token_keeper

from django import forms
from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm


class MyUserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 
                    'username', 
                    'first_name', 
                    'phone_number', 
                    'is_active',
                    'is_superuser']
    fieldsets = (
        ("Registeration", {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active','is_superuser','is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('id',)
    filter_horizontal = ()


class TokenAdmin(admin.ModelAdmin):
    list_display = ['User','access_token', 'refresh_token','allowed']

# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
admin.site.register(Token_keeper, TokenAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
