from django.core.files.base import ContentFile
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class CategorySerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = Category
        fields = ('id',)
        read_only_fields = ('id',)


class CommentSerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = Comment


class GenreSerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = Genre


class GenreTitleSerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = GenreTitle


class ReviewSerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = Review


class TitleSerialiser(serializers.ModelSerializer):
    ...

    class Meta:
        model = Title
