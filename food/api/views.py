from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.utils import timezone

from kitchen.settings import paystack_key
from food.models import (Dish, 
                         OrderInfo, 
                         PaymentHistory, 
                         Cart, 
                         OrderEntry)

from .serializers import (  DishListSerializer,
                            CarListSerializer,
                            OrderEntrySerializer,
                            OrderDetailSerializer,
                            OrderListSerializer, 
                            OrderCreateSerializer,
                            CartDetailSerializer)


class DishView(generics.ListAPIView):
    """
    List all the items in cart for a specific user
    """
    queryset            = Dish.objects.filter(active=True, date_available__gte=timezone.now().date())
    serializer_class    = DishListSerializer


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


class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
                            
    serializer_class            = CartDetailSerializer

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return Cart.objects.filter(customer_name=the_user)

    def perform_update(self, serializer):
        dish_inp = serializer.validated_data.get('dish')
        qty = serializer.validated_data.get('qty')
        add = serializer.validated_data.get('address')
        dda = serializer.validated_data.get('delivery_date')
        dish_obj = Dish.objects.filter(name__iexact=dish_inp).first()
        serializer.save(dish=dish_obj,
                        delivery_date=dda,
                        qty=qty,
                        total_cost=dish_obj.price * qty,
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

        cus_ = request.user

        # Expecting a list as data
        data_ = request.data
        if type(data_) != list:
            data_ = [data_]
        
        # Check if dish is still available
        dish_list = [line['dish'] for line in data_]
        delivery_list = [line['delivery_date'] for line in data_]

        for dl, dv_l in zip(dish_list, delivery_list):
            qs = Dish.objects.filter(name__iexact=dl, date_available=dv_l)
            if not qs.exists():
                return Response({'Error': f"{dl} is no longer available on {dv_l}"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        email = self.request.user.email
        amount = sum([line['total_cost'] for line in data_])
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
        if len(data_) == 1:
            dish_mod = Dish.objects.filter(name__iexact=data_[0].get('dish')).first()
            OrderInfo.objects.create(
                order_info = order_obj,
                customer_name = cus_,
                address = data_[0].get('address'),
                dish = dish_mod,
                qty = data_[0].get('qty'),
                total_cost = dish_mod.price * data_[0].get('qty'),
                delivery_date = data_[0].get('delivery_date')
            )
        else:
            final_list = []
            for item in data_:
                dish_model = Dish.objects.filter(name__iexact=item.get('dish')).first()

                cart_obj = OrderInfo(
                    order_info = order_obj,
                    customer_name = cus_,
                    address = item.get('address'),
                    dish = dish_model,
                    qty = item.get('qty'),
                    total_cost = dish_model.price * item.get('qty'),
                    delivery_date = item.get('delivery_date')
                )
                final_list.append(cart_obj)
            OrderInfo.objects.bulk_create(final_list)

        # Delete orders from cart
        for item in data_:
            Cart.objects.filter(id=item['id']).delete()

        return Response(resp.json())


class VerifyPaymentView(APIView):
    def post(self, request):
        ref = request.data.get("reference")
        link = "https://api.paystack.co/transaction/verify/" + ref
        headers = {'Content-Type': 'application/json',
                    'Authorization' : 'Bearer ' + paystack_key}

        resp = requests.get(link, headers=headers)

        if resp.status_code != 200:
            return Response({'Error': "Paystack error",
                            "status_code": resp.status_code}, 
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # If response returns a success, update the payment history
        # Update the OrderEntry table

        status_message = resp.json()['data']['status']

        qs = PaymentHistory.objects.filter(reference__iexact=ref)
        if not qs.exists():
            return Response({'message' : 'Payment History with payment ref does not exist'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        qs.update(status=status_message,
                payment_channel=resp.json()['data']['channel'],
                transaction_date=resp.json()['data']['transaction_date'],
                verify_status=resp.json()['status']
        )

        old_ref = qs.first().order_info.payment_ref
        order_entry_qs = OrderEntry.objects.filter(payment_ref__iexact=old_ref)
        order_entry_qs.update(status=status_message,
                              payment_ref = ref)

        return Response({'response': status_message, 'url':qs.first().authorization_url}, 
                        status=status.HTTP_200_OK)


# To avoid overflow of information, two views will be created to address 
# User seeing items he has already paid for
class OrderEntryView(generics.ListAPIView):
    """
    Lists the overview of orders that have been placed by a user
    """
    serializer_class    = OrderEntrySerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        return OrderEntry.objects.filter(customer_name=the_user)


class OrderInfoView(generics.ListAPIView):
    """
    Lists the details of orders that have been placed by a user
    """
    serializer_class    = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filter results to return only user's Orders
        """
        the_user = self.request.user
        the_id = self.kwargs.get('pk')
        return OrderInfo.objects.filter(customer_name=the_user, order_info=the_id)


class PaymentRetryView(APIView):
    def post(self, request):

        cus_ = request.user

        # Expecting a list as data
        data_ = request.data
        if type(data_) != list:
            data_ = [data_]

        # Check if dish is still available 
        for dl, dv_l in zip(dish_list, delivery_list):
            qs = Dish.objects.filter(name__iexact=dl, date_available=dv_l)
            if not qs.exists():
                return Response({'Error': f"{dl} is no longer available on {dv_l}"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        order_obj = OrderEntry.objects.get(pk=data_[0].get('order_info'))
        email = self.request.user.email
        amount = sum([line['total_cost'] for line in data_])
        link = "https://api.paystack.co/transaction/initialize"
        

        headers = {'Content-Type': 'application/json',
                    'Authorization' : 'Bearer ' + paystack_key}
        data = {"email": email, "amount": amount * 100}

        resp = requests.post(link, headers = headers, json=data)

        # First validate the response came back with 200
        if resp.status_code != 200:
            return Response({'Error': "Paystack error"}, 
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        PaymentHistory.objects.create(
            order_info = order_obj,
            customer  = self.request.user,
            amount_paid = amount,
            authorization_url= resp.json()['data']['authorization_url'],
            access_code = resp.json()['data']['access_code'],
            reference = resp.json()['data']['reference'],
        )

        return Response(resp.json())

# Without a payment atempt, status is abandoned
# Failed transaction response, status comes back as failed
# As long as trx in not successful, pay_url will always work

# User wants to see items he has already paid for
# User wants to retry payment for failed items 

# Need to ensure that when ever payment view is called, we check if 
# dish is actually available