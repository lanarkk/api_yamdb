from django.db import models

LENGTH_LIMIT = 21


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug[:LENGTH_LIMIT]


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug[:LENGTH_LIMIT]


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    rating = models.IntegerField('Рейтинг', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


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
