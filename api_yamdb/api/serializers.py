from django.db.models import Avg
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
        return int(rating.get('score__avg'))


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ()
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже поcтавили оценку этому произвднию',
            )
        ]
