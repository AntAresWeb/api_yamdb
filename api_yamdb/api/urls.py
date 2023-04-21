from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet,
                    GenreViewSet, CategoryViewSet)


router = routers.DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
router.register(r'titles/(?P<title_id>\d+)/reviews/?P<review_id>\d+/comments',
                CommentViewSet, basename='comment')
# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
router.register('genries', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
