from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


admin.site.empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель Категории в админ зоне.
    Описывает ее внешний вид и функционал."""

    list_display = ('name', 'slug', )
    search_fields = ('name', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', )
    search_fields = ('name', )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Модель произведения в админ зоне.
    Описывает ее внешний вид и функционал."""

    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
        'genre_list'
    )
    list_editable = ('name', 'year', 'description', 'category',)
    search_fields = ('year', 'name', )
    list_filter = ('category', )

    def genre_list(self, obj):
        if obj.genre.all():
            return list(obj.genre.all().values_list('name', flat=True))


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Модель Отзыва в админ зоне.
    Описывает ее внешний вид и функционал."""

    list_display = (
        'text',
        'pub_date',
        'author',
        'title',
        'score',
    )
    list_editable = ('text',)
    search_fields = ('text', 'score',)
    list_filter = ('author', 'score',)
    list_display_links = ('author', 'title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель комментария в админ зоне.
    Описывает ее внешний вид и функционал."""

    list_display = (
        'text',
        'pub_date',
        'author',
        'review',
    )
    list_editable = ('text',)
    search_fields = ('text', )
    list_filter = ('author', 'review',)
    list_display_links = ('author', 'review',)
