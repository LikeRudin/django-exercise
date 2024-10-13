from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("password", views.ChangePassword.as_view(), name="change-password"),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("<int:pk>", views.PublicUser.as_view()),
    path("<int:pk>/tweets", views.TweetsByUser.as_view())
]