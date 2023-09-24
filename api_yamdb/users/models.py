from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        # Нужны пустые строки до и после класса.
        # дима
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
        max_length=128,
        # Максимальную длину можно подсчитывать "на лету".
        # Если в будущем нужно будет заводить еще роли,
        # то тут не придется править. В генераторе списка подсчитываем
        # длины ролей, максимальная будет граничным значением.
        # дима
        choices=Roles.choices,
        default=Roles.USER,
    )

    class Meta:
        ordering = ('date_joined',)
        # Для поля username нужна валидация на "me".
        # дима
