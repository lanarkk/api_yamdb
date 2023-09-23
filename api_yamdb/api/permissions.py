# TODO дописать пермишн "владелец аккаунта или нет доступа"
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self,
                       request,
                       view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)

        return (
            request.method in permissions.SAFE_METHODS
            or is_admin
            or (request.user.is_authenticated and request.user.role == "admin")
        )


class IsAuthorAuthenticatedOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):
    """Права доступа для авторизованного пользователя или операций чтения.

    Допускает частичное изменение и удаление пользователем своих
    собственных объектов (отзыва и комментария к нему).
    Модератор и администратор могут также изменять и удалать чужие материалы.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (
            request.user.role == 'user'
            and obj.author == request.user
        ):
            return True
        elif (
            (
                request.user.role in ['moderator', 'admin']
                or request.user.is_superuser
            )
            and view.action in ['partial_update', 'destroy']
        ):
            return True
