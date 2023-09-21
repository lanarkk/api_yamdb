# TODO в url добавить пути для users/me/ и users/{username}/ 
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import Signup, Auth, UserDetailView

router = DefaultRouter()
router.register('signup', Signup, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', Auth.as_view()),
    path('users/me/', UserDetailView.as_view()),
    path('users/<str:username>/', UserDetailView.as_view()),
]
