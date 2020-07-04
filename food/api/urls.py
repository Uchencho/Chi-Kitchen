from .views import UserOrders
from django.urls import path, include

app_name = "food"

urlpatterns = [
    path('myorders/', UserOrders.as_view(), name='orders'),
]
