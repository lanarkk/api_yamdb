from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewset,
    GenreViewset,
    TitleViewset
)

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewset, basename='categories')
router_v1.register('genres', GenreViewset, basename='genres')
router_v1.register('titles', TitleViewset, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
