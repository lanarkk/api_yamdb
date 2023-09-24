from django.contrib import admin

from reviews.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
# Так как наш проект управляется командой администраторов,
# админ-части также стоить уделить внимание.
# Заводим все модели, настраиваем классы.
# дима

# На странице списка изменений пользователей
# стоит добавить возможность менять роль.
# дима
