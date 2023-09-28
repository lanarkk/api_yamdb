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
        # Валидация на me повторяется в нескольких местах,
        # можно вынести в отдельную функцию. макс

    def validate_me_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Ты не можешь использовать "me" в качестве имени!'
            )


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    # Нужно ограничить поля по длине. макс
    confirmation_code = serializers.CharField(max_length=64)
