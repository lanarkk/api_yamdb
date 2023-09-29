from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        self.validate_me_username(value)
        return value

    def validate_me_username(self, username):
        # Выносим в validators.py, используем в 2-х местах.
        if username == 'me':
            raise serializers.ValidationError(
                'Ты не можешь использовать "me" в качестве имени!'
            )


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGHT)
    confirmation_code = serializers.CharField(
        max_length=settings.CODE_MAX_LENGHT
    )
