from .views import (
                    OrderInfoView, 
                    CreateDishView, 
                    DishDetailView,
                    PaymentHistoryAdminView
                    )
from django.urls import path, include

app_name = "backoffice"

urlpatterns = [
    path('orderinfo/', OrderInfoView.as_view(), name='orderinfo'),
    path('dish/', CreateDishView.as_view(), name='dish'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='editdish'),
    path('payments/', PaymentHistoryAdminView.as_view(), name='dish'),
]
