import string
from random import choice

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    # У джанго есть механизм для генерации токенов default_token_generator.
    # Посмотрите в эту сторону. Не придется хранить токен в БД.
    code = ''.join(choice(characters) for _ in range(length))
    return code


def send_verification_code(confirmation_code, user_email):
    send_mail(
        subject='Код подтверждения регистрации',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='production@yandex.ru',
        # Емейл отправителя письма выносим в константу в настройках приложения.
        recipient_list=[user_email],
        fail_silently=True,
    )


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }
