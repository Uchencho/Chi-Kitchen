from django.contrib import admin
from .models import User

from django import forms
from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm


class MyUserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 
                    'username', 
                    'first_name', 
                    'phone_number', 
                    'is_active',
                    'is_superuser']
    # list_filter = ('is_admin',)
    fieldsets = (
        ("Registeration", {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'first_name')}),
        ('Permissions', {'fields': ('is_active','is_superuser',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
