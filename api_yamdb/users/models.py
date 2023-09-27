from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

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
        if (
            self.role == self.Roles.ADMIN
            or self.is_superuser or self.is_staff
        ):
            return True
        return False

    @property
    def is_reg_user(self):
        if self.role == self.Roles.USER:
            return True
        return False

    @property
    def is_admin_or_moder(self):
        if (self.is_admin or self.role == self.Roles.MODERATOR):
            return True
        return False
