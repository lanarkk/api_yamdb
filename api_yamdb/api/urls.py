from django.db import router
from django.urls import include, path

from api_yamdb.api import views

router.register('users', views.UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users.urls'))
]