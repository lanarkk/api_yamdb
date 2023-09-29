from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.validators import validate_me_username, validate_username


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        USER: str = 'user'
        MODERATOR: str = 'moderator'
        ADMIN: str = 'admin'

    username = models.CharField(
        max_length=settings.USERNAME_MAX_LENGHT, unique=True,
        validators=[validate_username, validate_me_username]
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=settings.CODE_MAX_LENGHT,
        editable=True,
    )
    bio = models.TextField(
        _('user biography'),
        blank=True,
        default=''
    )

    role = models.CharField(
        _('user role'),
        max_length=max(len(role) for role, _ in Roles.choices),
        choices=Roles.choices,
        default=Roles.USER,
    )

    class Meta:
        ordering = ('date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    @property
    def is_admin(self):
        return (self.role == self.Roles.ADMIN
                or self.is_superuser or self.is_staff)

    @property
    def is_admin_or_moder(self):
        return self.is_admin or self.role == self.Roles.MODERATOR
