from accounts.models import User
from .serializers import RegisterSerializer

import requests

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from kitchen.settings import CLIENT_SECRET, CLIENT_ID

BASE_URL = 'http://localhost:8000/'

class RegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []


class LoginView(APIView):
    permission_classes  = []
    
    def post(self, request):
        r = requests.post(
            BASE_URL + 'o/token/',
            data = {
                'grant_type' : 'password',
                'username' : request.data.get('username'),
                'password' : request.data.get('password'),
                'client_id' : CLIENT_ID,
                'client_secret' : CLIENT_SECRET,
            },
        )
        return Response(r.json())
