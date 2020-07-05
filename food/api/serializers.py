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



class OrderCreateSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    dish              = serializers.CharField()

    class Meta:
        model = Order
        fields = [
            "id",
            'customer_name',
            'dish',
            'time_of_order', 
            'updated', 
            'address', 
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

    def validate(self, data):
        """
        Validates that the total price is more than the price of the food
        """
        dish_name = data.get("dish")
        total_cost = data.get("total_cost")
        dish_model = Dish.objects.filter(name__iexact=dish_name).first()
        if total_cost < dish_model.price:
            raise serializers.ValidationError({"Total Cost" : "Total cost cannot be less than cost of dish"})
        return data

    def create(self, validated_data):
        """
        Overwrites the create method because of foreign key issues
        """
        context = self.context['request']
        cus_ = context.user
        dish_model = Dish.objects.filter(name__iexact=validated_data.get('dish')).first()
        
        ord_obj = Order.objects.create(
            customer_name = cus_,
            address = validated_data.get('address'),
            dish = dish_model,
            total_cost = validated_data.get('total_cost')
        )
        return ord_obj