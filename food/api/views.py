from rest_framework import generics, status, permissions

from food.models import Dish, Order
from .serializers import (
                            OrderListSerializer, 
                            OrderCreateSerializer,
                            OrderDetailSerializer)

class UserOrdersView(generics.ListAPIView):
    """
    List all the orders of a specific user
    """
    serializer_class    = OrderListSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Order.objects.filter(customer_name=the_user)


class CreateOrderView(generics.CreateAPIView):
    """
    Create an order
    """
    serializer_class    = OrderCreateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Order.objects.filter(customer_name=the_user)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
                            
    serializer_class            = OrderDetailSerializer

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Order.objects.filter(customer_name=the_user)

    def perform_update(self, serializer):
        dish_inp = serializer.validated_data.get('dish')
        qty = serializer.validated_data.get('qty')
        add = serializer.validated_data.get('address')
        tot = serializer.validated_data.get('total_cost')
        dish_obj = Dish.objects.filter(name__iexact=dish_inp).first()
        serializer.save(dish=dish_obj,
                        qty=qty,
                        total_cost=tot,
                        address=add)

    def put(self, request, *args, **kwargs):
        """
        Edit a user's Order
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a User's Order
        """
        return self.destroy(request, *args, **kwargs)