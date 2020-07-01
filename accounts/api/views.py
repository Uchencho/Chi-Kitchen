from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer

import requests
from django.utils import timezone

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

        email = request.data.get('username')
        qs = User.objects.filter(email__iexact=email)
        if not qs.exists():
            content = {
                    "message": "User with email address does not exist"
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        r = requests.post(
            BASE_URL + 'o/token/',
            data = {
                'grant_type' : 'password',
                'username' : email,
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
            user_model = qs.first()
            content = r.json()
            content['id'] = user_model.id
            content['fullname'] = user_model.first_name + " " + user_model.last_name
            content["last_login"] = user_model.last_login.strftime("%d-%b-%Y")
            content["date_joined"] = user_model.date_joined.strftime("%d-%b-%Y")

            user_model.last_login = timezone.now()
            user_model.save()

            return Response(content, status=status.HTTP_200_OK)
