from rest_framework import serializers

from food.models import OrderInfo, Dish, Cart

class CarListSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    customer_email    = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField(source='dish.name', read_only=True)
    dish_cost         = serializers.IntegerField(source='dish.price', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 
            'customer_name',
            'customer_email', 
            'dish',
            'dish_cost',
            'time_of_order', 
            'updated', 
            'delivery_date',
            'address', 
            'qty', 
            'total_cost'
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def get_customer_email(self, obj):
        context = self.context['request']
        return context.user.email

class OrderListSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    customer_email    = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField(source='dish.name', read_only=True)
    dish_cost         = serializers.IntegerField(source='dish.price', read_only=True)

    class Meta:
        model = OrderInfo
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
            'payment_status'
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def get_customer_email(self, obj):
        context = self.context['request']
        return context.user.email


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Add items to cart for payment
    """
    customer_name     = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField()
    total_cost        = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 
            'customer_name', 
            'dish',
            'delivery_date',
            'address', 
            'qty', 
            'total_cost'
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username



class OrderDetailSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField()

    class Meta:
        model = OrderInfo
        fields = [
            "id",
            'customer_name',
            'dish',
            'time_of_order', 
            'updated', 
            'address',
            'qty', 
            'total_cost',
            'payment_status',
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def validate_dish(self, value):
        qs = Dish.objects.filter(name__iexact=value)
        if not qs.exists():
            raise serializers.ValidationError("Dish does not exist. Kindly create first.")
        return value

    def validate(self, data):
        """
        Validates that the total price is more than the price of the food
        """
        dish_name = data.get("dish")
        total_cost = data.get("total_cost")
        qty = data.get("qty")

        dish_model = Dish.objects.filter(name__iexact=dish_name).first()
        if total_cost < dish_model.price:
            raise serializers.ValidationError({"Total Cost" : "Total cost cannot be less than cost of dish"})
        elif total_cost < (dish_model.price * qty):
            raise serializers.ValidationError({"Total Cost" : "Total cost cannot be less than unit cost multiplied by qty"})
        return data



# [{
#     "dish": "Pounded Yam and Egusi Soup",
#     "delivery_date": "2020-07-14",
#     "address": "Lagos",
#     "qty": 3
# },

# {
#     "dish": "Pounded Yam and Egusi Soup",
#     "delivery_date": "2020-07-14",
#     "address": "Abuja",
#     "qty": 7
# }]