from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet,
                    GenreViewSet, CategoryViewSet)

router = DefaultRouter()
router.register('reviews', ReviewViewSet)
router.register(r'reviews/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('genries', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

'''


'''
