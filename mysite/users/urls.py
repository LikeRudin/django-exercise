from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("<str:username>", views.PublicUser.as_view())
]