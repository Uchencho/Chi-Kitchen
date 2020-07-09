from rest_framework import serializers

from food.models import Order, Dish

class OrderListSerializer(serializers.ModelSerializer):
    customer_name     = serializers.SerializerMethodField(read_only=True)
    customer_email    = serializers.SerializerMethodField(read_only=True)
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
            'payment_status'
        ]

    def get_customer_name(self, obj):
        context = self.context['request']
        return context.user.username

    def get_customer_email(self, obj):
        context = self.context['request']
        return context.user.email


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
            'qty', 
            'total_cost',
            'payment_status'
        ]
        read_only_fields = ['payment_status']

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

    def create(self, validated_data):
        """
        Overwrites the create method because of foreign key issues
        """
        context = self.context['request']
        cus_ = context.user
        dish_model = Dish.objects.filter(name__iexact=validated_data.get('dish')).first()

    #   Cannot bulk create because of the relationship to other tables
    #   Order.objects.bulk_create([
    #     Order(
    #         customer_name = jh,
    #         address = add,
    #         dish = first_dish,
    #         qty = 2,
    #         total_cost = 15000
    #     ),
    #     Order(
    #         customer_name = jh,
    #         address = add,
    #         dish = second_dish,
    #         qty = 3,
    #         total_cost = 18000
    #     )
    # ])

        ord_obj = Order.objects.create(
            customer_name = cus_,
            address = validated_data.get('address'),
            dish = dish_model,
            qty = validated_data.get('qty'),
            total_cost = validated_data.get('total_cost'),
            payment_status = 'Pending'
        )
        return ord_obj


class OrderDetailSerializer(serializers.ModelSerializer):
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