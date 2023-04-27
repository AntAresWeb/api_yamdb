from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.utils import name_is_valid
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerialiser(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug',)
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }


class GenreSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug',)
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    year = serializers.IntegerField(
        max_value=datetime.now().year,
        required=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'name': {'required': True, 'max_length': 256},
            'rating': {'required': False, 'read_only': True, 'default': None},
            'description': {'allow_blank': True}
        }


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerialiser(many=True, read_only=True)
    genre.fields = ('slug',)
    category = CategorySerialiser(read_only=True)
    year = serializers.IntegerField(
        max_value=datetime.now().year,
        required=True
    )


    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'name': {'required': True, 'max_length': 256},
            'year': {'required': True},
            'rating': {'required': False, 'read_only': True},
            'description': {'allow_blank': True},
            'genre': {'required': True},
            'category': {'required': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

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


class UserSerializer(serializers.ModelSerializer):
    '''Сериализер api/v1/users/'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        extra_kwargs = {
            'username': {'required': True, 'max_length': 150},
            'email': {'required': True, 'max_length': 254},
            'first_name': {'allow_blank': True, 'max_length': 150},
            'last_name': {'allow_blank': True, 'max_length': 150},
            'role': {'default': 'user'}
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('username', 'email'),
                message=("Пользователь с указанными именем или адресом есть.")
            )
        ]

    def validate_username(self, value):
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        if isinstance(value, str) and len(value) == 0:
            raise serializers.ValidationError('Имя указывать обязательно.')
        return value

    def validate_email(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise serializers.ValidationError('e-mail указывать обязательно.')
        try:
            obj = self.Meta.model.objects.get(email=value)
        except self.Meta.model.DoesNotExist:
            return value
        if self.instance and obj.id == self.instance.id:
            return value
        else:
            raise serializers.ValidationError('Этот e-mail уже ииспользуется')


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)
        extra_kwargs = {
            'username': {'required': True, 'max_length': 150},
            'email': {'required': True, 'max_length': 254},
            'first_name': {'allow_blank': True, 'max_length': 150},
            'last_name': {'allow_blank': True, 'max_length': 150},
            'role': {'default': 'user'}
        }

    def validate_username(self, value):
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value


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
