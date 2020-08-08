from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from accounts.models import Token_keeper

class IsTokenValid(permissions.BasePermission):
    message = "Token has expired because you logged out, please login again"

    def has_permission(self, request, view):
        user = request.user
        is_allowed_user = True

        try:
            token = get_authorization_header(request).decode('utf-8').split(" ")[1]
        except IndexError:
            return False
        qs = Token_keeper.objects.filter(User=user, 
                                        access_token=token,
                                        allowed = False)
        if qs.exists():
            is_allowed_user = False
        return is_allowed_user


class BasicToken(permissions.BasePermission):
    message = "No token was passed"

    def has_permission(self, request, view):
        token = "c6acc7ddb4e23e275382d3eea89fae82fee144e598e7728fc3daf418a78daa77"
        try:
            in_token = get_authorization_header(request).decode('utf-8').split(" ")[1]
        except IndexError:
            return False
        if token != in_token:
            return False
        return True