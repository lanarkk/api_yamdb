from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    # Хорошим тоном считается оставить документацию к классу. Так и поступим. макс
    ADMIN_ROLE = 'admin'

    def is_admin(self, user):
        return user.role == self.ADMIN_ROLE or user.is_superuser

    def has_permission(self, request, view):# Нужна пустая строка. А нужен ли перенос?   дима
        return (
            request.user.is_authenticated
            and self.is_admin(request.user)
        )
        # Использовать хардкод не очень хорошо, в любой момент мы
        # можем поменять название роли на какое-нибудь другое, и нам
        # надо не забыть поменять его везде. Роли пользователей лучше
        # вынести в отдельные константы, например ADMIN = 'admin'.
        # Предлагаю в модели сделать метод is_admin который будет
        # возвращать булево при всех возможных вариантах админов(роль,
        # супер, стафф). Также метод лучше сделать свойством) класса.
        # дима


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        #Одноразовая переменна. дима
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
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
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.role == 'user'
                and obj.author == request.user
            )
            or (
                (
                    request.user.role in ['moderator', 'admin']
                    or request.user.is_superuser
                )
                and view.action in ['partial_update', 'destroy']
            )
        )
        # С помощью логического оператора or можно объединить проверки
        # и сделать один возврат. Стоит учесть, что вычисление следующего
        # операнда после or будет только в случае если
        # предыдущий будет равен False. дима
