from .views import OrderInfoView
from django.urls import path, include

app_name = "backoffice"

urlpatterns = [
    path('orderinfo/', OrderInfoView.as_view(), name='orderinfo'),
]
