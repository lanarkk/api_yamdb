from django.urls import path

from users.views import Auth, Signup

urlpatterns = [
    path('signup/', Signup.as_view()),
    path('token/', Auth.as_view()),
]
