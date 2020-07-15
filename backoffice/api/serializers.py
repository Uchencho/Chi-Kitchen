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


class OrderInfoSerializer(serializers.ModelSerializer):
    customer_name   = UserSerializer(read_only=True)
    order_info      = serializers.CharField(source='order_info.status', read_only=True)
    dish            = serializers.CharField(source='dish.name', read_only=True)

    class Meta:
        model = OrderInfo
        fields = [
            'id',  
            'dish',
            'order_info',
            'delivery_date',
            'address', 
            'qty', 
            'total_cost',
            'customer_name',
        ]