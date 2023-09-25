from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

DISPLAY_LIMIT = 21
CHAR_MAX_LENGHT = 256
SLUG_MAX_LENGHT = 50
RATING_MAX_POINT = 10
RATING_MIN_POINT = 1
RATING_DEFAULT_POINT = 0

User = get_user_model()


class CatGenModel(models.Model):
    """Абстрактная модель для моделей из категории и жанра."""

    name = models.CharField('Название', max_length=CHAR_MAX_LENGHT)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGHT, unique=True)

    class Meta:
        abstract = True
        ordering = ('slug',)


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


class Category(CatGenModel):
    """Модель категорий."""

    class Meta(CatGenModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug[:DISPLAY_LIMIT]


class Genre(CatGenModel):
    """Модель жанров."""

    class Meta(CatGenModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug[:DISPLAY_LIMIT]


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField('Название', max_length=CHAR_MAX_LENGHT)
    year = models.IntegerField('Год выпуска')
    # Тут лучше использовать PositiveSmallIntegerField. Будет
    # занимать меньше места в БД.
    # Не хватает валидации, что год не больше текущего.
    # Чтобы ускорить поиск произведений по году,
    # лучше добавить индекс. Как это работает.
    # https://im-cloud.ru/blog/chto-takoe-indeksy-bazy-dannyh-dlja-nachinajushhih/
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#positivesmallintegerfield
    # лиля
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
        return self.name[:DISPLAY_LIMIT]


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
    score = models.IntegerField(
        'Рейтинг',
        validators=[
            MaxValueValidator(
                limit_value=RATING_MAX_POINT,
                message='Не более 10 баллов.'
            ),
            MinValueValidator(
                limit_value=RATING_MIN_POINT,
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

    def __str__(self):
        return self.text[:DISPLAY_LIMIT]


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

    def __str__(self):
        return self.text[:DISPLAY_LIMIT]
