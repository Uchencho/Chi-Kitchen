from rest_framework import serializers

from accounts.models import User
from food.models import OrderInfo, Dish, Cart, OrderEntry, PaymentHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 
                  'first_name', 
                  'last_name', 
                  'phone_number', 
                ]

class OrderEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEntry
        fields = ['status']


class OrderInfoSerializer(serializers.ModelSerializer):
    customer_name = UserSerializer(read_only=True)
    order_info = OrderEntrySerializer(read_only=True)

    class Meta:
        model = OrderInfo
        fields = [
            'id',  
            'dish',
            'delivery_date',
            'address', 
            'qty', 
            'total_cost',
            'customer_name',
            'order_info',
        ]