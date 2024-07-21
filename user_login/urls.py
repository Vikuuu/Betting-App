from django.urls import path
from .views import UserLoginView, UserView, RefreshTokenView, LogoutView


urlpatterns = [
    path("login", UserLoginView.as_view(), name="login"),
    path("user", UserView.as_view(), name="user"),
    path("refresh", RefreshTokenView.as_view(), name="refresh"),
    path("logout", LogoutView.as_view(), name="logout"),
]
