from rest_framework import serializers


def validate_username(value):
    username = value.get('username')
    if username and username == 'me':
        raise serializers.ValidationError(
            "Нельзя использовать 'me' в качестве имени пользователя."
        )
    return value
