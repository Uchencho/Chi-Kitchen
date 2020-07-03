from django.contrib import admin
from .models import Dish

# Register your models here.
class DishAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'active', 'dish_type', 'date_available', 'tag']

admin.site.register(Dish, DishAdmin)