import mailbox
import os
import string
from random import choice

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(choice(characters) for _ in range(length))
    return code


def send_verification_email(to_email, verification_code):
    subject = 'Код подтверждения регистрации'
    message = f'Ваш код подтверждения: {verification_code}'

    if not os.path.exists('sent_emails'):
        os.makedirs('sent_emails')

    mbox = mailbox.mbox('sent_emails')

    msg = mailbox.mboxMessage()
    msg.set_unixfrom('author')
    msg['From'] = 'your_email@example.com'  # заменить надо емейл
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_payload(message)

    mbox.add(msg)
    mbox.flush()

    print(f'Письмо сохранено в локальной папке'
          f'для {to_email}')


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
