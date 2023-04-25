from django.db.models import Avg
import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, views
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import IsAuthorModeratorAdminOrReadOnly, IsAdminOrReadOnly
from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title,
                            User)
from api.serializers import (CategorySerialiser,
                             CommentSerializer,
                             GenreSerialiser,
                             ReviewSerializer,
                             TitleSerializer,
                             UserSignupSerializer, TitleCreateSerializer)




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
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class AuthSignupView(views.APIView):
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
            try:
                user = get_object_or_404(User, username=username)
                if email != user.email:
                    response['email'] = ['Не совпадает с регистрационным.']
                    return Response(response,
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User.objects.create(username=username, email=email)
            user.confirmation_code = str(uuid.uuid4())
            user.save()
            send_mail('Авторизация в YaMDB',
                      f'''
                      Уважаемый {user.username}!
                      Вы успешно прошли регистрацию на сервисе YaMDB.
                      Высылаем вам код активаци для получения токена:
                      {user.confirmation_code}
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


class AuthTokenView(views.APIView):
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        response = {}
        if 'username' not in request.data:
            response['username'] = ['Обязательное поле.']
        if 'confirmation_code' not in request.data:
            response['confirmation_code'] = ['Обязательное поле.']
        if len(response) > 0:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                response['confirmation_code'] = ['Неверный код подтверждения.']
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            status_code = status.HTTP_200_OK
            response = {
                'token': token
            }

            return Response(response, status=status_code)
