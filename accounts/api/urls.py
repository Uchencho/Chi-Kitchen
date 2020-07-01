from .views import (
                    RegisterAPIView, 
                    LoginView, 
                    LogoutView)
from django.urls import path, include

from oauth2_provider.views import RevokeTokenView

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', RevokeTokenView.as_view(), name='logout'),
]
