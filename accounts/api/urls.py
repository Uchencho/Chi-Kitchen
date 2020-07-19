from .views import (
                    RegisterAPIView, 
                    LoginView, 
                    LogoutView)
from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', RevokeTokenView.as_view(), name='logout'),
]
