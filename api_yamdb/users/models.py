from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):# Нужны пустые строки до и после класса. дима

    class Roles(models.TextChoices):
        USER: str = 'user'
        MODERATOR: str = 'moderator'
        ADMIN: str = 'admin'

    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=64,
        editable=True,
    )
    bio = models.TextField(
        _('user biography'),
        blank=True,
        default=''
    )

    def get_max_role_length(self):
        return max(len(role) for role, _ in self.Roles.choices)
    # Максимальную длину можно подсчитывать "на лету".
    # Если в будущем нужно будет заводить еще роли,
    # то тут не придется править. В генераторе списка подсчитываем
    # длины ролей, максимальная будет граничным значением.
    # дима

    role = models.CharField(
        _('user role'),
        max_length=get_max_role_length,
        choices=Roles.choices,
        default=Roles.USER,
    )

    class Meta:
        ordering = ('date_joined',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
        # Для поля username нужна валидация на "me".
        # дима
