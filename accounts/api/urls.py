from .views import (
                    RegisterAPIView,
                    ProfileDetailApiView,
                    LoginView,
                    RefreshTokenView, 
                    LogoutView)
from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetailApiView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
