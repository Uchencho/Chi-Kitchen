from .views import (UserCartView,
                    DishView,
                    VerifyPaymentView,
                    OrderEntryView, 
                    CreateOrderView,
                    OrderDetailAPIView,
                    PaymentCheckoutView)
from django.urls import path, include

app_name = "food"

urlpatterns = [
    path('dish/', DishView.as_view(), name='dish'),
    path('mycart/', UserCartView.as_view(), name='cart'),
    path('mycart/add/', CreateOrderView.as_view(), name='addCart'),
    path('mycart/<int:pk>/', OrderDetailAPIView.as_view(), name='editcart'),
    path('myorders/', OrderEntryView.as_view(), name='orders'),
    path('myorders/checkout/', PaymentCheckoutView.as_view(), name='checkout'),
    path('myorders/verify/', VerifyPaymentView.as_view(), name='verify')
]
