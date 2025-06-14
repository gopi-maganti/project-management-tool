from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.restful.viewsets.auth_viewset import AuthViewSet, FacebookLogin, GoogleLogin
from api.restful.viewsets.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/facebook/", FacebookLogin.as_view(), name="facebook_login"),
]
