from rest_framework import serializers
import regex as re


def validate_me_username(username):
    # Выносим в validators.py, используем в 2-х местах.
    if username == 'me':
        raise serializers.ValidationError(
            'Ты не можешь использовать "me" в качестве имени!'
        )


def validate_username(username):
    pattern = r'^[\w.@+-]+$'
    if not re.fullmatch(pattern, username):
        raise serializers.ValidationError(
            'Введенный вами логин содержит недопустимые символы!'
        )
