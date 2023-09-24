from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'slug',
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'year',
        'description',
        'category',
        'genre',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    fields = (
        'title',
        'text',
        'pub_date',
        'author',
        'score',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    fields = (
        'review',
        'author',
        'text',
        'pub_date',
    )

# Так как наш проект управляется командой администраторов,
# админ-части также стоить уделить внимание.
# Заводим все модели, настраиваем классы.
# Для произведений желательна возможность редактировать
# категории прямо в листе произведений. Кроме того нужно вывести
# список жанров через запятую в листе произведений
# (для этого придется написать метод).
