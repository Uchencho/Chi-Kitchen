from .views import (UserCartView,
                    DishView,
                    VerifyPaymentView,
                    # UserOrdersView, 
                    CreateOrderView,
                    OrderDetailAPIView,
                    PaymentCheckoutView)
from django.urls import path, include

app_name = "food"

urlpatterns = [
    path('dish/', DishView.as_view(), name='dish'),
    path('mycart/', UserCartView.as_view(), name='cart'),
    # path('myorders/', UserOrdersView.as_view(), name='orders'),
    path('myorders/create/', CreateOrderView.as_view(), name='orders'),
    path('mycart/<int:pk>/', OrderDetailAPIView.as_view(), name='editorder'),
    path('myorders/checkout/', PaymentCheckoutView.as_view(), name='checkout'),
    path('myorders/verify/', VerifyPaymentView.as_view(), name='verify')
]
