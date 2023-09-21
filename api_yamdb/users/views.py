# TODO Добавить вью для users/me/ и users/{username}/
# if kwargs.get('username') == me дя заметки
# обрабатываются одним классом
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from users.services import send_verification_code, generate_verification_code
from users.serializers import (
    AuthSerializer,
    SignUpSerializer,
    ProfileSerializer
)
from users.services import get_tokens_for_user

User = get_user_model()


class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer  # акт мой сериалайзер

    def retrieve(self, request, *args, **kwargs):
        # Является ли запрашиваемое имя пользователя "me"
        if kwargs:
            if User.objects.filter(
                username=self.kwargs.get('username')
            ).exists():
                if self.request.user.role == 'admin':
                    user = get_object_or_404(
                        User,
                        username=self.kwargs.get('username'),
                    )
                else:
                    return Response(
                        {'detail': 'У вас недостаточно прав.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            else:
                return Response(
                    {'detail': 'Пользователь не найден.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            user = self.request.user

        serializer = self.get_serializer(user)
        return Response(serializer.data)


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


class Signup(mixins.CreateModelMixin,
             viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def perform_create(self, serializer, user=User):
        confirmation_code = generate_verification_code()
        serializer.save(
            confirmation_code=confirmation_code
        )
        send_verification_code(
            user_email=serializer.data['email'],
            confirmation_code=confirmation_code,
        )
