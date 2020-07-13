from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from kitchen.settings import paystack_key
from food.models import Dish, OrderInfo, PaymentHistory, Cart
from .serializers import (  CarListSerializer,
                            OrderListSerializer, 
                            OrderCreateSerializer,
                            OrderDetailSerializer)

class UserCartView(generics.ListAPIView):
    """
    List all the items in cart for a specific user
    """
    serializer_class    = CarListSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Cart.objects.filter(customer_name=the_user)


class CreateOrderView(generics.CreateAPIView):
    """
    Adds items to cart for payment
    """
    serializer_class    = OrderCreateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Cart.objects.filter(customer_name=the_user)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
                            
    serializer_class            = OrderDetailSerializer

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return OrderInfo.objects.filter(customer_name=the_user)

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


class PaymentCheckoutView(APIView):

    def post(self, request):

        order_id = self.request.data.get("id")
        email = self.request.user.email
        amount = self.request.data.get("amount", 0)
        link = "https://api.paystack.co/transaction/initialize"

        headers = {'Content-Type': 'application/json',
                    'Authorization' : 'Bearer ' + paystack_key}
        data = {"email": email, "amount": amount}

        resp = requests.post(link, headers = headers, json=data)

        PaymentHistory.objects.create(
            the_order = Order.objects.get(pk=order_id),
            customer  = self.request.user,
            amount_paid = int(amount) / 100,
            authorization_url= resp.json()['data']['authorization_url'],
            access_code = resp.json()['data']['access_code'],
            reference = resp.json()['data']['reference'],
        )

        return Response({'response': "Updated Successfully",
                        'data' : resp.json()})