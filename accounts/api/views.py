from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer

import requests
from django.utils import timezone

from rest_framework import generics, status, permissions
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []


class LoginView(TokenObtainPairView):
    """
    Login endpoint that returns access token and refresh token
    """
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes      = [permissions.IsAuthenticated]

    def post(self, request):
        '''
        Method to revoke tokens.
        {"token": "<token>"}
        '''
        # r = requests.post(
        #     'http://0.0.0.0:8000/o/revoke_token/', 
        #     data={
        #         'token': request.data['token'],
        #         'client_id': CLIENT_ID,
        #         'client_secret': CLIENT_SECRET,
        #     },
        # )
        # # If it goes well return sucess message (would be empty otherwise) 
        # if r.status_code == requests.codes.ok:
        #     return Response({'message': 'token revoked'}, r.status_code)
        # # Return the error if it goes badly
        # return Response(r.json(), r.status_code)
        # https://medium.com/@halfspring/guide-to-an-oauth2-api-with-django-6ba66a31d6d
        print("helloooo", get_authorization_header(request))
        return Response(status=status.HTTP_200_OK)