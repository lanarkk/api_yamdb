# TODO дописать пермишн "владелец аккаунта или нет доступа"
from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить GET-запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить изменение или удаление объекта только владельцу или администратору
        return obj.owner == request.user or request.user.role == 'admin'


class IsAdmin(permissions.BasePermission):
    def has_permission(self,
                       request,
                       view):
        return (
            request.user.is_authenticated and (request.user.role == 'admin')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self,
                       request,
                       view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self,
                       request,
                       view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self,
                              request,
                              view,
                              obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return any([
            obj.author == request.user,
            request.user.role in ['moderator', 'admin']
        ])
