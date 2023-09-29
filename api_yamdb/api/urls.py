from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewset, CommentViewSet, GenreViewset,
                    ReviewViewSet, TitleViewset, UsersViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewset, basename='categories')
router_v1.register('genres', GenreViewset, basename='genres')
router_v1.register('titles', TitleViewset, basename='titles')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='reviews'
)
urls_v1 = [
    path('', include(router_v1.urls)),
    path('auth/', include('users.urls'))
]
urlpatterns = [
    path('v1/', include(urls_v1)),
]
