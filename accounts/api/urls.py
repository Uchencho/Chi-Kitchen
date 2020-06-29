from .views import RegisterAPIView
from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
]
