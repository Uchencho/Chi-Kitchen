from accounts.models import User, Token_keeper
from .serializers import  (
                            RegisterSerializer,
                            LoginSerializer,
                            RefreshSerializer
                        )

from rest_framework import generics, status, permissions
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsTokenValid
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []


class LoginView(TokenObtainPairView):
    """
    Login endpoint that returns access token and refresh token
    """
    serializer_class = LoginSerializer


class RefreshTokenView(TokenRefreshView):
    """
    Login endpoint that returns access token and refresh token
    """
    serializer_class = RefreshSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class LogoutView(APIView):
    permission_classes      = [permissions.IsAuthenticated]

    def post(self, request):
        '''
        Method to revoke tokens.
        {"refresh": "<refresh_token>"}
        '''
        user = request.user
        access = get_authorization_header(request).decode('utf-8').split(" ")[1]
        refresh = request.data.get("refresh")
        qs = Token_keeper.objects.filter(
            User = user,
            access_token = access,
            refresh_token = refresh,
        )
        if not qs.exists():
            return Response({"message" : "Invalid credentials"},
                            status = status.HTTP_400_BAD_REQUEST)
        qs.update(allowed=False)
        return Response(status=status.HTTP_200_OK)