from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from kitchen.settings import paystack_key
from food.models import (Dish, 
                         OrderInfo, 
                         PaymentHistory, 
                         Cart, 
                         OrderEntry)

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

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(CreateOrderView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Cart.objects.filter(customer_name=the_user)

    def check_data(self, data):
        """
        Validates that the Delivery date is inline with dish availability
        """
        dish_list = [line['dish'] for line in data]
        delivery_list = [line['delivery_date'] for line in data]

        for dl, dv_l in zip(dish_list, delivery_list):
            qs = Dish.objects.filter(name__iexact=dl, date_available=dv_l)
            if not qs.exists():
                return False, f"{dl} is not available on {dv_l}"

        return True, "Success"


    def post(self, request):
        """
        Overwrites the create method because of foreign key issues
        """

        data_ = request.data
        if type(data_) != list:
            data_ = [data_]

        if not self.check_data(data_)[0]:
            return Response({
            'message' : self.check_data(data_)[1]}, status=status.HTTP_400_BAD_REQUEST)
    
        cus_ = request.user

        if len(data_) == 1:
            dish_mod = Dish.objects.filter(name__iexact=data_[0].get('dish')).first()
            Cart.objects.create(
                customer_name = cus_,
                address = data_[0].get('address'),
                dish = dish_mod,
                qty = data_[0].get('qty'),
                total_cost = dish_mod.price * data_[0].get('qty'),
                delivery_date = data_[0].get('delivery_date')
            )
            return Response({'message' : 'Created successfully'}, 
                                status=status.HTTP_201_CREATED)

        final_list = []
        for item in data_:
            dish_model = Dish.objects.filter(name__iexact=item.get('dish')).first()

            cart_obj = Cart(
                customer_name = cus_,
                address = item.get('address'),
                dish = dish_model,
                qty = item.get('qty'),
                total_cost = dish_model.price * item.get('qty'),
                delivery_date = item.get('delivery_date')
            )
            final_list.append(cart_obj)
        Cart.objects.bulk_create(final_list)
        return Response({
            'message' : 'Created successfully'}, status=status.HTTP_201_CREATED)


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

    # Sum up total cost of items for checkout
    # Do a post request to paystack
    # Create order entries, info and details, two tables
    # Create payment history entry
    # Delete orders from cart
    

    def post(self, request):

        email = self.request.user.email
        amount = sum([line['total_cost'] for line in self.request.data])
        link = "https://api.paystack.co/transaction/initialize"
        

        headers = {'Content-Type': 'application/json',
                    'Authorization' : 'Bearer ' + paystack_key}
        data = {"email": email, "amount": amount * 100}

        resp = requests.post(link, headers = headers, json=data)

        # First validate the response came back with 200
        if resp.status_code != 200:
            return Response({'Error': "Paystack error"}, 
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Create order entry, not details
        order_obj = OrderEntry.objects.create(
            customer_name = self.request.user,
            dish = ", ".join([line['dish'] for line in self.request.data]),
            total_cost = amount,
            payment_ref = resp.json()['data']['reference']
            )

        PaymentHistory.objects.create(
            order_info = order_obj,
            customer  = self.request.user,
            amount_paid = amount,
            authorization_url= resp.json()['data']['authorization_url'],
            access_code = resp.json()['data']['access_code'],
            reference = resp.json()['data']['reference'],
        )

        # For loop to create order information

        # Delete orders from cart

        return Response({'response': "Updated Successfully",
                        'data' : resp.json()})