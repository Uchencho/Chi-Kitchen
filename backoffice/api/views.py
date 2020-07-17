from rest_framework import generics, permissions

from .serializers import OrderInfoSerializer, CreateDishSerializer
from food.models import OrderInfo, Dish, Cart, OrderEntry, PaymentHistory


class OrderInfoView(generics.ListAPIView):
    permission_class        = [permissions.IsAdminUser]
    serializer_class        = OrderInfoSerializer
    queryset                = OrderInfo.objects.all()
    search_fields           = ['order_info__status', 'delivery_date']


class CreateDishView(generics.ListCreateAPIView):
    permission_class        = [permissions.IsAdminUser]
    serializer_class        = CreateDishSerializer
    queryset                = Dish.objects.all()
    search_fields           = ['name', 'active', 'tag', 'date_available']

# Insert pagination on each backoffice view
# create dish view