from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.validators import validate_username

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = (validate_username,)


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGHT)
    confirmation_code = serializers.CharField(
        max_length=settings.CODE_MAX_LENGHT
    )
