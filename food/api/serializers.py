from rest_framework import serializers

from food.models import Order

class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'customer_name', 
            'dish', 
            'time_of_order', 
            'updated', 
            'address', 
            'total_cost',
        ]