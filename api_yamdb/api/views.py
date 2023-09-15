from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from api.serializers import UserSerializer

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = get_all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
