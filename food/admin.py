from django.contrib import admin
from .models import Dish, Order, PaymentHistory, Cart

# Register your models here.
class DishAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'active', 
                    'dish_type', 'date_available', 'tag']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'dish', 'time_of_order', 
                     'address', 'qty', 'total_cost']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount_paid', 'status', 
                    'access_code','authorization_url', 'reference', 
                    'payment_channel', 'transaction_date', 'verify_status']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'dish', 'time_of_order', 
                     'updated', 'delivery_date','address', 
                     'qty', 'total_cost']

admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentHistory, PaymentAdmin)
admin.site.register(Cart, CartAdmin)