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
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Значение не может быть me.')
        return value

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        print('---->')
        return data

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        
        return auth_user


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = User.objects.get(username=username)

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
