from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()

router.register('categories', views.CategoryViewSet, basename='category')
router.register('genres', views.GenreViewSet, basename='genre')
router.register('titles', views.TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                '/comments', views.CommentViewSet, basename='comment')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('auth/signup/', views.AuthSignupView.as_view(), name='signup'),
    path('auth/token/', views.AuthTokenView.as_view(), name='token'),
    path('users/me/', views.UserMeDetailUpdateAPIView.as_view(), name='userme'),
    path('drf-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
