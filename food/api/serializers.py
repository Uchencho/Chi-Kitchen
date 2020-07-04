from rest_framework import serializers

from food.models import Order, Dish

class OrderListSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    customer_email    = serializers.SerializerMethodField(read_only=True)
    time_of_order     = serializers.SerializerMethodField(read_only=True)
    updated           = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField(source='dish.name', read_only=True)
    dish_cost         = serializers.IntegerField(source='dish.price', read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            'customer_name',
            'customer_email', 
            'dish',
            'dish_cost', 
            'time_of_order', 
            'updated', 
            'address', 
            'total_cost',
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def get_customer_email(self, obj):
        context = self.context['request']
        return context.user.email

    def get_time_of_order(self, obj):
        context = self.context['request']
        order_model = Order.objects.filter(customer_name=context.user).first()
        return order_model.time_of_order.strftime("%d-%b-%Y %H:%M")

    def get_updated(self, obj):
        context = self.context['request']
        order_model = Order.objects.filter(customer_name=context.user).first()
        return order_model.updated.strftime("%d-%b-%Y %H:%M")