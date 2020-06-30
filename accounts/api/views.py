from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer

import requests

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from kitchen.settings import CLIENT_SECRET, CLIENT_ID

BASE_URL = 'http://localhost:8000/'

class RegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []


class LoginView(APIView):
    serializer_class    = LoginSerializer
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
        if r.json().get("error_description") == "Invalid credentials given.":
            content = {
                    "message": "Invalid credentials given."
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            email = request.data.get('username')
            user_model = User.objects.filter(email__iexact=email).first()
            content = r.json()
            content['id'] = user_model.id
            content['fullname'] = user_model.first_name + " " + user_model.last_name
            return Response(content, status=status.HTTP_200_OK)
