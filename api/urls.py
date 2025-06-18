from django.urls import path

from api.restful.viewsets.user_viewset import GoogleLoginViewSet, UserViewSet

urlpatterns = [
    path(
        "user/register/", UserViewSet.as_view({"post": "create"}), name="user-register"
    ),
    path("user/login/", UserViewSet.as_view({"post": "login_jwt"}), name="user-login"),
    path(
        "user/token/", UserViewSet.as_view({"post": "login_token"}), name="token-login"
    ),
    path("user/logout/", UserViewSet.as_view({"post": "logout"}), name="user-logout"),
    path("user/list/", UserViewSet.as_view({"get": "list_users"}), name="user-list"),
    path(
        "user/profile/",
        UserViewSet.as_view({"get": "list_current_user"}),
        name="user-data",
    ),
    path("user/google/", GoogleLoginViewSet.as_view(), name="google-login"),
]
