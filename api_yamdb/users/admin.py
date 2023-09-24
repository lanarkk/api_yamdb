from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
# Так как наш проект управляется командой администраторов,
# админ-части также стоить уделить внимание.
# Заводим все модели, настраиваем классы.

# На странице списка изменений пользователей
# стоит добавить возможность менять роль.
