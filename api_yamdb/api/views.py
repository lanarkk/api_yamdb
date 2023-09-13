from django.shortcuts import get_object_or_404, get_list_or_404, render
from rest_framework import generics, viewsets

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Title


class ViewsetsGenericsMixin(
    viewsets.GenericViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView
):
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

    def create_or_update(self, serializer):
        category_slug = serializer.initial_data.get('category')
        genres = serializer.initial_data.get('genre')
        kwargs = {}
        if category_slug:
            kwargs['category'] = get_object_or_404(
                Category, slug=category_slug)
        if genres:
            kwargs['genre'] = get_list_or_404(Genre, slug__in=genres)

        serializer.save(**kwargs)

    def perform_create(self, serializer):
        self.create_or_update(serializer)

    def perform_update(self, serializer):
        self.create_or_update(serializer)
