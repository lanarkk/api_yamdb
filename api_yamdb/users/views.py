from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.services import send_verification_code, generate_verification_code
from users.serializers import AuthSerializer, SignUpSerializer
from users.services import get_tokens_for_user

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
