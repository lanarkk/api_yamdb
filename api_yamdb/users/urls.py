from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views


router = DefaultRouter()
router.register('signup', views.Signup)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.Auth.as_view())
]
