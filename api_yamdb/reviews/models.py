from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import validate_year


User = get_user_model()


class CatGenModel(models.Model):
    """Абстрактная модель для моделей из категории и жанра."""

    name = models.CharField('Название', max_length=settings.CHAR_MAX_LENGHT)
    slug = models.SlugField(
        'Слаг', max_length=settings.SLUG_MAX_LENGHT, unique=True
    )

    class Meta:
        abstract = True
        ordering = ('slug',)

    def __str__(self):
        return self.slug[:settings.DISPLAY_LIMIT]


class RevComModel(models.Model):
    """Абстрактная модель для отзывов и комментариев."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:settings.DISPLAY_LIMIT]


class Category(CatGenModel):
    """Модель категорий."""

    class Meta(CatGenModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CatGenModel):
    """Модель жанров."""

    class Meta(CatGenModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField('Название', max_length=settings.CHAR_MAX_LENGHT)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.DISPLAY_LIMIT]


class TitleGenre(models.Model):
    """Таблица для отношения многие-ко-многим в паре произведение-жанр."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',
        null=True
    )


class Review(RevComModel):
    """Модель отзыва. Создает в
    бд таблицу с отзывами.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MaxValueValidator(
                limit_value=settings.RATING_MAX_POINT,
                message='Не более 10 баллов.'
            ),
            MinValueValidator(
                limit_value=settings.RATING_MIN_POINT,
                message='Не менее 1 балла.'
            ),
        ]
    )

    class Meta(RevComModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]


class Comment(RevComModel):
    """Модель Комментария. Создает в
    бд таблицу с комментариями к отзывам.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(RevComModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = "comments"
