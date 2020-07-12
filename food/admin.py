from django.contrib import admin
from .models import Dish, OrderInfo, PaymentHistory, Cart, OrderEntry

# Register your models here.
class DishAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'active', 
                    'dish_type', 'date_available', 'tag']

class OrderInfoAdmin(admin.ModelAdmin):
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

class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'status', 'time_of_order', 
                     'total_cost']

admin.site.register(Dish, DishAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderEntry, OrderEntryAdmin)
admin.site.register(PaymentHistory, PaymentAdmin)
admin.site.register(Cart, CartAdmin)