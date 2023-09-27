from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('category', 'genre')


class ObjRelatedField(serializers.SlugRelatedField):
    # Лишний класс. Достаточно to_representation переопределить в
    # TitleSerializer и вернуть в нем TitleReadOnlySerializer
    # подставив в него instance. лиля

    def to_representation(self, value):
        if isinstance(value, Category):
            serializer = CategorySerializer(value)
        elif isinstance(value, Genre):
            serializer = GenreSerializer(value)
        else:
            raise Exception(
                'Запрос содержит неожиданные данные.'
            )
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = ObjRelatedField(  # Подойдет стандартное SlugRelatedField. лиля
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = ObjRelatedField(  # Подойдет стандартное SlugRelatedField. лиля
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):  # Есть в проекте validate_year
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Указанный год выпуска произведения еще не наступил.'
            )
        return value

    def create(self, validated_data):
        # Лишний метод. лиля
        genres = validated_data.pop('genre')
        title = Title.objects.create(
            **validated_data
        )
        for genre in genres:
            TitleGenre.objects.create(
                title=title,
                genre=genre
            )
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзыва."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Комментария."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('review',)
