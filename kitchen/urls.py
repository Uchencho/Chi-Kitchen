
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    path('api/food/', include('food.api.urls', namespace='api-food')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
