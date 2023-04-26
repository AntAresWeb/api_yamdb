from django.db.models import Avg
import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, views, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (AllowAny,
                                        IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import IsAuthorModeratorAdminOrReadOnly, IsAdminOrReadOnly
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
                             TitleCreateSerializer,
                             UserSerializer,
                             UserMeSerializer,
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
    queryset = Category.objects.all()
    serializer_class = CategorySerialiser
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    # get post del
    queryset = Genre.objects.all()
    serializer_class = GenreSerialiser
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    # get post patch del
    queryset = Title.objects.annotate(rating=Avg('reviews__score')
                                      ).all().order_by('-year',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''Контроллер запросов api/v1/users/'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserMeDetailUpdateAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMeSerializer
    lookup_field = 'username'

    def get(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)


class AuthSignupView(views.APIView):
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        response = {}
        for field in ('username', 'email'):
            if field not in request.data:
                response[field] = ['Обязательное поле.']
        if len(response) > 0:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                if email != user.email:
                    response['email'] = ['Не совпадает с регистрационным.']
                    return Response(response,
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                if User.objects.filter(email=email).exists():
                    response['email'] = ['Такой e-mail уже занят.']
                    return Response(response,
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
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
            return Response(serializer.validated_data, status=status_code)


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
