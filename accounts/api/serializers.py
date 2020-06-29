from accounts.models import User

from rest_framework import serializers


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