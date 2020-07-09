from .views import (
                    UserOrdersView, 
                    CreateOrderView,
                    OrderDetailAPIView,
                    PaymentCheckoutView)
from django.urls import path, include

app_name = "food"

urlpatterns = [
    path('myorders/', UserOrdersView.as_view(), name='orders'),
    path('myorders/create/', CreateOrderView.as_view(), name='orders'),
    path('myorders/<int:pk>/', OrderDetailAPIView.as_view(), name='editorder'),
    path('myorders/checkout/', PaymentCheckoutView.as_view(), name='checkout')
]
