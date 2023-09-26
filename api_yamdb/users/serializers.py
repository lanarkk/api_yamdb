from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            # Валидация на me повторяется в нескольких местах,
            # можно вынести в отдельную функцию. макс
            raise serializers.ValidationError(
                'Ты не можешь использовать me в качестве имени!'
            )
        return value


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    # Нужно ограничить поля по длине. макс
    confirmation_code = serializers.CharField()
