from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


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
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score', default=0))
<<<<<<< HEAD
        return int(rating.get('score__avg'))
=======
        return rating.get('score__avg')
>>>>>>> origin/develop


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
