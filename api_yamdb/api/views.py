from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import (IsAdmin, IsAdminUserOrReadOnly,
                             IsAuthorAuthenticatedOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class ViewsetsGenericsMixin(
    # Хорошо. Стоит вынести в отдельный файл - mixins.py.
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """Создает класс (миксин) обобщенного вьюсета.

    Он допускает только выдачу списка объектов, создание и удаление объкета.
    В нем настроен поиск по полю 'name'.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class AllowedMethodsMixin(viewsets.ModelViewSet):
    """Создает миксин с настроенными допустимыми методами (все, кроме PUT)."""

    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]


class UsersViewSet(AllowedMethodsMixin):
    """Обрабатывает запросы к users/ и users/{username}/."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)


class ProfileViewSet(APIView):
    # Лучше реализовать users/me/ через декоратор action в UsersViewSet,
    # не придется переписывать два метода,
    # обойдемся условием и избавимся от дублирующих строк.
    """Обрабатывает запросы к users/me/."""

    def get(self, request):
        if request.user.is_authenticated:
            # Можно воспользоваться стандартным пермишеном.
            user = get_object_or_404(
                User,
                username=request.user.username
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Неавторизованный пользователь'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(
                User,
                username=request.user.username
            )
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                # У метода is_valid есть параметр-флаг raise_exception,
                # если его поставить в True, то можно избавиться
                # от проверок, метод вернет ошибки валидации.
                serializer.save(role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CategoryViewset(ViewsetsGenericsMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly, )


class GenreViewset(ViewsetsGenericsMixin):
    # Обратите внимание, что еще можно убрать в миксин.
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly, )


class TitleFilter(FilterSet):
    # Это класс фильтрации, лучше создать файл с
    # "говорящим" названием и вынести код туда
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewset(AllowedMethodsMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminUserOrReadOnly,)

    def fetch_read_only_fields_data(self, serializer):
        """Получает из запроса жанры и категорию произведения.

        Если таковые присутствуют в запросе, возвращает
        соотевтетсвующие им объекты или список объектов БД.
        """
        category_slug = serializer.initial_data.get('category')
        try:
            genres = serializer.initial_data.getlist('genre')
        except AttributeError:
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
# Предлагаю написать еще один сереализатор для произведения,
# будет один для создания/обновления, один для вывода,
# тут просто выбирать в зависимости от запроса. Код сильно похудеет.


class ReviewViewSet(AllowedMethodsMixin):
    """Вьюсет для модели Ревью."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorAuthenticatedOrReadOnly,
    )

    def get_title(self):
        """Возвращает объект тайтла или выдает 404."""
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        # Валидацию выносим в сериализатор.
        review = Review.objects.filter(
            title=self.get_title(),
            author=self.request.user
        ).exists()
        if review:
            raise serializers.ValidationError(
                'Нельзя оставить больше одного '
                'отзыва на одно произведение!'
            )
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(AllowedMethodsMixin):
    """Вьюсет для модели Комментария."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorAuthenticatedOrReadOnly,
    )

    def get_review(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )  # Лишний запрос, все можно сделать в одном.
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
