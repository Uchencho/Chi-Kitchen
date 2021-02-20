
from django.contrib import admin
from django.urls import path, include

from .views import HealthCheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck', HealthCheck.as_view()),
    path('api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    path('api/food/', include('food.api.urls', namespace='api-food')),
    path('api/backoffice/', include('backoffice.api.urls', namespace='api-backoffice')),
]
