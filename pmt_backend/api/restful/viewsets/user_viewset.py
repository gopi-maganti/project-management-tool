from typing import cast

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserData
from api.restful.serializers.user_serializer import (
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet to handle registration, login (token + JWT), and user listing.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "login_token", "login_jwt"]:
            return [AllowAny()]
        return [IsAuthenticated()]


    @action(detail=False, methods=["post"], url_path="register")
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response("User created"),
            400: openapi.Response("Incomplete or invalid data"),
        },
        operation_description="Register a new user",
    )
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User registered successfully",
                    "token": token.key,
                    "user": UserRegisterSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["post"], url_path="login-token")
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: openapi.Response("Login successful")},
        operation_description="Login using username and password with DRF Token",
    )
    def login_token(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "message": "Login successful",
                    "user": UserRegisterSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


    @action(detail=False, methods=["post"], url_path="login-jwt")
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful with JWT",
                examples={
                    "application/json": {
                        "refresh": "refresh_token_here",
                        "access": "access_token_here",
                        "user": {
                            "id": 1,
                            "username": "sample",
                            "email": "sample@email.com",
                        },
                    }
                },
            ),
            400: "Bad Request",
        },
        operation_description="Login with JWT (username & password)",
    )
    def login_jwt(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = cast(dict, serializer.validated_data)
            user = authenticate(
                username=validated_data.get("username"),
                password=validated_data.get("password"),
            )
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": UserRegisterSerializer(user).data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["post"], url_path="logout", permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"refresh": openapi.Schema(type=openapi.TYPE_STRING)},
            required=["refresh"]
        ),
        responses={200: "Token blacklisted successfully"},
        operation_description="Logout by blacklisting the refresh token"
    )
    def logout_jwt(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["get"], url_path="list")
    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        operation_description="List all users (requires authentication)",
    )
    def list_users(self, request):
        users = UserData.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="profile")
    @swagger_auto_schema(
        responses={
            200: openapi.Response("User data retrieved successfully"),
            401: openapi.Response("Authentication credentials were not provided."),
        },
        operation_description="Retrieve current user profile (requires authentication)",
    )
    def list_current_user(self, request):
        user = request.user
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLoginViewSet(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
