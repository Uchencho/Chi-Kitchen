from rest_framework import generics, status, permissions

from food.models import Dish, Order
from .serializers import OrderListSerializer

class UserOrders(generics.ListAPIView):
    queryset            = Order.objects.all()
    serializer_class    = OrderListSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Order.objects.filter(customer_name=the_user)