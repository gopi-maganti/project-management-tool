from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import CharField, ChoiceField, Serializer


class UsernameLoginSerializer(Serializer):
    username = CharField()
    password = CharField()


class TokenLoginSerializer(Serializer):
    token = CharField()


class LoginChoiceSerializer(Serializer):
    login_type = ChoiceField(
        choices=[
            ("username", "Username & Password"),
            ("token", "Token-based Login"),
            ("google", "Google SSO"),
            ("facebook", "Facebook SSO"),
        ]
    )


class AuthViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        method="post",
        request_body=LoginChoiceSerializer,
        responses={200: openapi.Response("Redirect endpoint provided")},
        operation_description="Choose login method and get redirected endpoint",
    )
    @action(detail=False, methods=["post"], url_path="login")
    def login_redirect(self, request):
        login_type = request.data.get("login_type")

        endpoint_map = {
            "username": "/auth/login/username/",
            "token": "/auth/login/token/",
            "google": "/auth/google/",
            "facebook": "/auth/facebook/",
        }

        if login_type in endpoint_map:
            return Response(
                {
                    "next": endpoint_map[login_type],
                    "message": f"Redirect to {endpoint_map[login_type]} for {login_type} login",
                }
            )

        return Response(
            {"detail": "Invalid login type"}, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        method="post",
        request_body=UsernameLoginSerializer,
        responses={200: openapi.Response("Login Successful")},
        operation_description="Login using username and password",
    )
    @action(detail=False, methods=["post"], url_path="login/username")
    def login_with_username(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    @swagger_auto_schema(
        method="post",
        request_body=TokenLoginSerializer,
        responses={200: openapi.Response("Login Successful")},
        operation_description="Login using token",
    )
    @action(detail=False, methods=["post"], url_path="login/token")
    def login_with_token(self, request):
        token_key = request.data.get("token")
        if not token_key:
            return Response(
                {"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = Token.objects.get(key=token_key)
            return Response({"token": token.key, "user_id": token.user.id})
        except Token.DoesNotExist:
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
