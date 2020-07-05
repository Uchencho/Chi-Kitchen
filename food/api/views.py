from rest_framework import generics, status, permissions

from food.models import Dish, Order
from .serializers import OrderListSerializer, OrderCreateSerializer

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