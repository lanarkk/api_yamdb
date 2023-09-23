# TODO написать сериализатор для новой модели
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Ты не можешь использовать me в качестве имени!'
            )
        return value


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
