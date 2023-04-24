from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre,
                            Review, Title)
from api.utils import name_is_valid


class CategorySerialiser(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id',)


class GenreSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id',)


class TitleSerialiser(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerialiser(read_only=True, many=True)
    category = CategorySerialiser(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                author=self.context['request'].user,
                title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return data


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Значение не может быть me.')
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(allow_blank=False)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Значение не может быть me.')
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value
