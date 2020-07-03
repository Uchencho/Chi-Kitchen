from django.contrib import admin
from .models import Dish, Order

# Register your models here.
class DishAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'active', 'dish_type', 'date_available', 'tag']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'dish', 'time_of_order', 'updated', 'address', 'total_cost']

admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)