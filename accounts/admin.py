from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'phone_number'] 

admin.site.register(User, UserAdmin)