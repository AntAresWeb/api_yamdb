from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .permissions import IsAuthorModeratorAdminOrReadOnly
from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)
from .serializers import (CategorySerialiser, CommentSerializer,
                          GenreSerialiser, GenreTitleSerialiser,
                          ReviewSerializer, TitleSerialiser)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # pagination_class = 
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    # pagination_class = 

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()


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


class TitleViewSet(viewsets.ModelViewSet):
    # get post patch del
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
