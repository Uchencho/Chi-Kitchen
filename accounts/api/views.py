from accounts.models import User, Token_keeper
from .serializers import  (
                            RegisterSerializer,
                            ProfileUpdateSerializer,
                            LoginSerializer,
                            RefreshSerializer
                        )

from rest_framework import generics, status, permissions
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterAPIView(generics.CreateAPIView):
    """
    Registers a user (creates a account)
    """
    queryset            = User.objects.all()
    serializer_class    = RegisterSerializer
    permission_classes  = []


class ProfileDetailApiView(generics.RetrieveUpdateAPIView):
    """
    Endpoint For Updating Profile
    """
    serializer_class    = ProfileUpdateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_queryset(self):
        """
        Return User's details
        """
        user_email = self.request.user.email
        return User.objects.filter(email__iexact=user_email)

    def put(self, request, *args, **kwargs):
        """
        Edit a user's Course
        """     
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Edit a user's Details
        """
        return self.partial_update(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    """
    Login endpoint that returns access token and refresh token
    """
    serializer_class = LoginSerializer


class RefreshTokenView(TokenRefreshView):
    """
    Refresh endpoint that returns refresh token
    """
    serializer_class = RefreshSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class LogoutView(APIView):
    """
    Logs out user by deactivating both access and refresh token
    """

    def post(self, request):
        '''
        Method to revoke tokens.
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