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
        null=True,
    )
    role = models.CharField(
        _('user role'),
        max_length=128,
        choices=Roles.choices,
        default=Roles.USER,
    )
