from rest_framework import generics, permissions

from .serializers import OrderInfoSerializer
from food.models import OrderInfo, Dish, Cart, OrderEntry, PaymentHistory


class OrderInfoView(generics.ListAPIView):
    permission_class        = [permissions.IsAdminUser]
    serializer_class        = OrderInfoSerializer
    queryset                = OrderInfo.objects.all()

# See orders that need to be delivered on a daily basis
# See user details per each order information