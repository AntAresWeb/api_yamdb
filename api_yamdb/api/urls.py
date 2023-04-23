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
router.register('signup/', views.SignupViewSet, basename='signup')
router.register('token/', views.TokenViewSet, basename='token')

urlpatterns = [
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
]
