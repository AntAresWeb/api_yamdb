from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)
from .serializers import (CategorySerialiser, CommentSerialiser,
                          GenreSerialiser, GenreTitleSerialiser,
                          ReviewSerialiser, TitleSerialiser)


class CategoryViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    # get post del
    queryset = Category.objects.all()
    serializer_class = CategorySerialiser
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(viewsets.ModelViewSet):
    # get post del
    queryset = Comment.objects.all()
    serializer_class = CommentSerialiser


class GenreViewSet(viewsets.ModelViewSet):
    # get post del
    queryset = Genre.objects.all()
    serializer_class = GenreSerialiser


class GenreTitleViewSet(viewsets.ModelViewSet):
    queryset = GenreTitle.objects.all()
    serializer_class = GenreTitleSerialiser


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialiser


class TitleViewSet(viewsets.ModelViewSet):
    # get post patch del
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
