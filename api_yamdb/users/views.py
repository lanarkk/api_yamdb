from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.serializers import AuthSerializer, SignUpSerializer
from users.services import (generate_verification_code, get_tokens_for_user,
                            send_verification_code)

User = get_user_model()


class Auth(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request):
        serializer: AuthSerializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            data = serializer.validated_data
            user = get_object_or_404(
                User,
                username=data.get('username'),
            )
            if user.confirmation_code != data.get('confirmation_code'):
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                get_tokens_for_user(user),
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class Signup(views.APIView):
    def post(self, request):
        """Отправляет код подтверждения пользователю при регистрации.

        При успешной регистрации создает нового пользователя и
        возвращает статус-код 200_OK.
        Допускает повторное обращение пользователя за кодом.
        """
        confirmation_code = generate_verification_code()

        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except ObjectDoesNotExist:
            user = None

        serializer = SignUpSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save(
                confirmation_code=confirmation_code
            )
            send_verification_code(
                user_email=serializer.validated_data['email'],
                confirmation_code=confirmation_code,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
