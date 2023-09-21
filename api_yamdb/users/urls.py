# TODO в url добавить пути для users/me/ и users/{username}/
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import Signup, Auth, UserProfileView

router = DefaultRouter()
router.register('signup', Signup, basename='signup')

auth_urls = [
    path('', include(router.urls)),
    path('token/', Auth.as_view()),
]
user_urls = [
    path('me/', UserProfileView.as_view()),
    path('<str:username>/', UserProfileView.as_view()),
]

urlpatterns = [
    path('users/', include(auth_urls)),
    path('auth/', include(auth_urls)),
]
