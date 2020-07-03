from oauth2_provider.views import RevokeTokenView
from django.urls import path, include

app_name = "food"

urlpatterns = [
    path('logout/', RevokeTokenView.as_view(), name='logout'),
]
