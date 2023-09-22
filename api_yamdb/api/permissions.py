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
