from rest_framework import generics, permissions

from .serializers import (OrderInfoSerializer, 
                          CreateDishSerializer,
                          RetrieveDishSerializer,
                          AllPaymentHistorySerializer
                          )
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


class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_class        = [permissions.IsAdminUser]
    serializer_class        = RetrieveDishSerializer
    queryset                = Dish.objects.all()

    def put(self, request, *args, **kwargs):
        """
        Edit a dish
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a dish
        """
        return self.destroy(request, *args, **kwargs)


class PaymentHistoryAdminView(generics.ListAPIView):
    permission_class        = [permissions.IsAdminUser]
    serializer_class        = AllPaymentHistorySerializer
    queryset                = PaymentHistory.objects.all()
    search_fields           = ['customer__email', 'payment_channel', 'transaction_date', 'status']

# Insert pagination on each backoffice view
# create dish view