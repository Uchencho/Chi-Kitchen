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


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                  'id',
                  'first_name', 
                  'last_name', 
                  'phone_number',
                  'email',
                  'is_active',
                  'is_superuser',
                  'is_staff',
                  'last_login',
                  'date_joined' 
                ]
        read_only_fields = ['last_login','date_joined']


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


class CreateDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            "id",
            'name', 
            'price', 
            'active', 
            'dish_type', 
            'date_available', 
            'tag'
        ]


class RetrieveDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'name', 
            'price', 
            'active', 
            'dish_type', 
            'date_available', 
            'tag'
        ]


class AllPaymentHistorySerializer(serializers.ModelSerializer):
    order_info      = serializers.CharField(source='order_info.dish', read_only=True)
    customer        = serializers.CharField(source='customer.email', read_only=True)
    class Meta:
        model = PaymentHistory
        fields = [
                  'customer',
                  'order_info',
                  'amount_paid', 
                  'status', 
                  'payment_channel', 
                  'transaction_date',
                  'access_code',
                  'reference',
        ]