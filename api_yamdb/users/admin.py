from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.empty_value_display = '-пусто-'


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Модель Пользователя в админ зоне.
    Описывает ее внешний вид и функционал."""

    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'password',
        'email',
        'role',
        'is_staff',
        'is_superuser',
        'bio',
        'date_joined',
    )
    list_editable = ('is_superuser', 'role', )
    search_fields = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
    )
    list_filter = (
        'email',
        'role',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
