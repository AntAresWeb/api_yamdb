from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .permissions import IsAuthorModeratorAdminOrReadOnly
from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User)
from api.serializers import (CategorySerialiser,
                             CommentSerializer,
                             GenreSerialiser,
                             ReviewSerializer,
                             TitleSerialiser,
                             UserSignupSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    # get post del
    queryset = Genre.objects.all()
    serializer_class = GenreSerialiser
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    # get post patch del
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    ...
