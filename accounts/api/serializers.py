from accounts.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    password            = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password    = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model   = User
        fields  = [
            'email',
            'password',
            'confirm_password',
        ]

    def validate(self, data):
        """
        Validates that the password are the same
        """
        pw  = data.get('password')
        pw2 = data.get('confirm_password')
        if pw != pw2:
            raise serializers.ValidationError("Passwords Must Match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()

        return user_obj


# class LoginSerializer(serializers.ModelSerializer):
#     password            = serializers.CharField(style={'input_type':'password'}, write_only=True)

#     class Meta:
#         model   = User
#         fields  = [
#             'username',
#             'password',
#         ]

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
    
        data = super(LoginSerializer, self).validate(attrs)

        #retrieve the user model and the student model
        user = User.objects.filter(username__iexact=self.user.username).first()

        try:
            last_login = user.last_login.strftime("%d-%b-%Y")
        except:
            last_login = user.date_joined.strftime("%d-%b-%Y")


        #update the response with id and username
        data.update({'id': self.user.id,
                    'username': self.user.username,
                    'First name' : self.user.first_name,
                    'Date registered' : user.date_joined.strftime("%d-%b-%Y"),
                    'last login' : last_login,    
        })

        self.user.last_login = timezone.now()
        self.user.save()

        return data
        