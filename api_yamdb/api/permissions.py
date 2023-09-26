from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    """Права доступа для админ-пользователя и суперпользователя.

    Допускает любые операции для админ-пользователя и суперпользователя,
    остальным запрещает любые операции.
    """
    ADMIN_ROLE = 'admin'  # Эта константа есть в классе Roles дима

    def is_admin(self, user):  # Выносим в модель Пользователя. дима
        # Также метод лучше сделать свойством класса.
        # https://pythonim.ru/osnovy/dekorator-svoystv-property-python](https://pythonim.ru/osnovy/dekorator-svoystv-property-python
        return user.role == self.ADMIN_ROLE or user.is_superuser

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and self.is_admin(request.user)  # Проверяем свойство.
        )


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    """Права доступа админ-пользователя, суперпользователя.

    Допускает любые операции для админ-пользователя и суперпользователя.
    Незарегистрированному пользователю, модератору и
    обычному пользователю доступны только безопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
            or (request.user.is_authenticated and request.user.role == "admin")
            # Вместо request.user.role == "admin" используем свойство is_admin
            # (оно у нас появится). дима
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
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.role == 'user'
                and obj.author == request.user
            )
            or (
                (
                    request.user.role in ['moderator', 'admin']
                    # Использовать хардкод не очень хорошо, в любой момент мы
                    # можем поменять название роли на какое-нибудь другое, и
                    # нам надо не забыть поменять его везде. Роли
                    # пользователей лучше вынести в отдельные константы,
                    # например ADMIN = 'admin'. Предлагаю в модели сделать
                    # метод is_admin который будет возвращать булево при всех
                    # возможных вариантах админов(роль, супер, стафф).
                    # Также метод лучше сделать свойством) класса. дима
                    or request.user.is_superuser
                )
                and view.action in ['partial_update', 'destroy']  # Лишнее.
            )
        )
