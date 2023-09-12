from django.shortcuts import get_object_or_404, get_list_or_404, render
from rest_framework import generics, viewsets

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Title


class CategoryViewset(
    viewsets.GenericViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewset(
    viewsets.GenericViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        category_slug = serializer.initial_data.pop('category')
        genres = serializer.initial_data.pop('genre')
        category = get_object_or_404(Category, slug=category_slug)
        genre_queryset = get_list_or_404(Genre, slug__in=genres)
        serializer.save(category=category, genre=genre_queryset)
