from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import TitleFilter
from api.mixins import AllowedMethodsMixin, ViewsetsGenericsMixin
from api.permissions import (IsAdmin, IsAdminUserOrReadOnly,
                             IsAuthorAuthenticatedOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadOnlySerializer, TitleSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class UsersViewSet(AllowedMethodsMixin):
    """Обрабатывает запросы к users/ и users/{username}/."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if '/me/' in self.request.path:
            return (permissions.IsAuthenticated(),)
        return (IsAdmin(),)

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewset(ViewsetsGenericsMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewset(ViewsetsGenericsMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly, )


class TitleViewset(AllowedMethodsMixin):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('name')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadOnlySerializer
        return TitleSerializer


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
        review = Review.objects.filter(  # Валидацию выносим в сериализатор. макс
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
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=get_object_or_404(  # Запрос не нужен, макс
                # просто self.kwargs.get('title_id')
                Title,
                pk=self.kwargs.get('title_id'),
            ),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
