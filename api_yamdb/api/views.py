from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, serializers, viewsets

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Review, Title


class ViewsetsGenericsMixin(
    viewsets.GenericViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView
):
    """Создает класс (миксин) обобщенного вьюсета.

    Он допускает только выдачу списка объектов, создание и удаление объкета.
    """

    pass


class CategoryViewset(ViewsetsGenericsMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewset(ViewsetsGenericsMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def fetch_read_only_fields_data(self, serializer):
        """Получает из запроса жанры и категорию произведения.

        Если таковые присутствуют в запросе, возвращает
        соотевтетсвующие им объекты или список объектов БД.
        """
        category_slug = serializer.initial_data.get('category')
        genres = serializer.initial_data.get('genre')
        kwargs = {}
        if category_slug:
            try:
                kwargs['category'] = Category.objects.get(slug=category_slug)
            except ObjectDoesNotExist:
                kwargs['category'] = None
        if genres:
            kwargs['genre'] = Genre.objects.filter(slug__in=genres)

        return kwargs

    def validate_read_only_fields(self, check_fields, **kwargs):
        """Проверят наличие обязательных полей и отвечающих им объектов БД."""
        errors = {}
        for field in check_fields:
            if field not in kwargs and self.request.method == 'POST':
                errors[field] = ['Обязательное поле.']
            elif field in kwargs and not kwargs[field]:
                errors[field] = ['Запрошенный объект не существует.']
        if errors:
            raise serializers.ValidationError(errors)

    def create_or_update(self, serializer):
        """Создает или изменяет запись о произведении."""
        kwargs = self.fetch_read_only_fields_data(serializer)
        self.validate_read_only_fields(
            check_fields=('category', 'genre'),
            **kwargs
        )
        serializer.save(**kwargs)

    def perform_create(self, serializer):
        self.create_or_update(serializer)

    def perform_update(self, serializer):
        self.create_or_update(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Ревью."""

    serializer_class = ReviewSerializer

    def get_title(self):
        """Возвращает объект тайтла или выдает 404."""
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Комментария."""

    serializer_class = CommentSerializer

    def get_review(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=title,
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
