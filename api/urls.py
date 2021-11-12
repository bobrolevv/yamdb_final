from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryListViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryListViewSet, basename='categoties')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/', include('auth.urls')),
    path('v1/', include(router.urls))
]
