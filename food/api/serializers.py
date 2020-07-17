from rest_framework import serializers

from food.models import OrderInfo, Dish, Cart, OrderEntry, PaymentHistory

class DishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = [
            'id', 
            'name', 
            'price',  
            'dish_type', 
            'date_available', 
            'tag'
        ]

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



class CartDetailSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField()
    total_cost        = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            'customer_name',
            'dish',
            'time_of_order',
            'delivery_date',
            'updated', 
            'address',
            'qty', 
            'total_cost',
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def validate_dish(self, value):
        qs = Dish.objects.filter(name__iexact=value)
        if not qs.exists():
            raise serializers.ValidationError("Dish does not exist. Kindly create first.")
        return value

    def validate(self, validated_data):
        dish_name = validated_data.get("dish")
        dd = validated_data.get("delivery_date")

        qs = Dish.objects.filter(name__iexact=dish_name, date_available=dd)
        if not qs.exists():
            raise serializers.ValidationError(f"{dish_name} is not available on {dd}.")
        return validated_data


class OrderEntrySerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderEntry
        fields = ['id', 
                  'customer_name', 
                  'status', 
                  'time_of_order',
                  'dish', 
                  'total_cost',
                  'payment_ref']

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username


class OrderDetailSerializer(serializers.ModelSerializer):
    dish            = serializers.CharField(source='dish.name', read_only=True)

    class Meta:
        model = OrderInfo
        fields = [
            'id',  
            'dish',
            'delivery_date',
            'address', 
            'qty', 
            'total_cost',
            'order_info'
        ]


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
                  'amount_paid', 
                  'status', 
                  'payment_channel', 
                  'transaction_date'
        ]


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