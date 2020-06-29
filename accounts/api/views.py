from accounts.models import User
from .serializers import RegisterSerializer

from rest_framework import generics


class RegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []