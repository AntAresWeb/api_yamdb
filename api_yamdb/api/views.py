from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, views
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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
                             UserSignupSerializer,
                             UserTokenSerializer)


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
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny,)


class SignupView(views.APIView):

    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        response = {}
        if 'email' not in request.data:
            response['email'] = ['Обязательное поле.']
        if 'username' not in request.data:
            response['username'] = ['Обязательное поле.']
        if len(response) > 0:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            serializer.save()
            user = User.objects.get(email=email, username=username)
            send_mail('Авторизация в YaMDB',
                      f'''
                      Уважаемый {user.username}!
                      Вы успешно прошли регистрацию на сервисе YaMDB.
                      Высылаем вам код активаци для получения токена.
                      Код активации: {user.password}
                      ''',
                      'admin@yamdb',
                      (user.email,),
                      fail_silently=False,)

            status_code = status.HTTP_200_OK
            response = {
                'email': serializer.data['email'],
                'username': serializer.data['username'],
            }

            return Response(response, status=status_code)
