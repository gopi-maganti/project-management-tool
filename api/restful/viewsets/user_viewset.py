from typing import cast
from pmt_backend.custom_logger import get_logger, log_exception
from api.utils import stringify_errors, pretty_print_errors

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

logger = get_logger(__name__).bind(module="user_viewset")

MAX_LOGIN_ATTEMPTS = 3

class UserViewSet(viewsets.ViewSet):
    """
    A Django ViewSet that handles user registration, login (Token and JWT), logout, and user retrieval.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Return the appropriate permissions depending on the action being performed.

        Returns:
            list: List of permission instances.
        """
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
        """
        Registers a new user.

        Args:
            request (HttpRequest): The HTTP request object containing user data.

        Returns:
            Response: HTTP response with status and data.

        Raises:
            Exception: If user creation or token generation fails.
        """
        logger.info("Registering new user", data={k: v for k, v in request.data.items() if k != "password"})
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                logger.info("User registered successfully", user_id=user.id)
                return Response(
                    {
                        "message": "User registered successfully",
                        "token": token.key,
                        "user": UserRegisterSerializer(user).data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                log_exception("User creation failed", e, module_name=__name__)
                return Response(
                    {"error": "Something went wrong"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        logger.warning("Invalid user registration data:\n" + pretty_print_errors(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login-token")
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: openapi.Response("Login successful")},
        operation_description="Login using username and password with DRF Token",
    )
    def login_token(self, request):
        """
        Authenticates user using Token-based authentication.

        Args:
            request (HttpRequest): Contains username and password.

        Returns:
            Response: Token and user info or error message.

        Raises:
            AuthenticationFailed: If credentials are invalid.
        """
        session = request.session
        attempts = session.get("login_attempts_token", 0)
        logger.info("Login token attempt", attempts=attempts, username=request.data.get("username"))

        if attempts >= MAX_LOGIN_ATTEMPTS:
            logger.warning("Max login attempts reached (token)", ip=request.META.get("REMOTE_ADDR"))
            return Response(
                {"error": "Maximum login attempts exceeded."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            session["login_attempts_token"] = 0
            logger.info("Token login successful", user_id=user.pk)
            return Response(
                {
                    "token": token.key,
                    "message": "Login successful",
                    "user": UserRegisterSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        session["login_attempts_token"] = attempts + 1
        logger.warning("Invalid token login credentials", username=username)
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
        """
        Authenticates user and returns JWT tokens.

        Args:
            request (HttpRequest): Contains username and password.

        Returns:
            Response: Access and refresh tokens or error message.

        Raises:
            AuthenticationFailed: If credentials are invalid.
        """
        session = request.session
        attempts = session.get("login_attempts_jwt", 0)
        logger.info("Login JWT attempt", attempts=attempts, username=request.data.get("username"))

        if attempts >= MAX_LOGIN_ATTEMPTS:
            logger.warning("Max login attempts reached (JWT)", ip=request.META.get("REMOTE_ADDR"))
            return Response(
                {"error": "Maximum login attempts exceeded."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

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
                session["login_attempts_jwt"] = 0
                logger.info("JWT login successful", user_id=user.pk)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": UserRegisterSerializer(user).data,
                    },
                    status=status.HTTP_200_OK,
                )

            session["login_attempts_jwt"] = attempts + 1
            logger.warning("Invalid JWT credentials", username=validated_data.get("username"))
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        logger.warning("JWT login validation failed", errors={k: str(v) for k, v in serializer.errors.items()})
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
    def logout(self, request):
        """
        Logs out the user by blacklisting their refresh token.

        Args:
            request (HttpRequest): Contains the refresh token.

        Returns:
            Response: Success or error message.

        Raises:
            Exception: If token is invalid or missing.
        """
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out", user_id=request.user.id)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception("Logout failed", e, module_name=__name__)
            return Response({"error": "Invalid or missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="list")
    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        operation_description="List all users (requires authentication)",
    )
    def list_users(self, request):
        """
        Retrieves a list of all registered users.

        Args:
            request (HttpRequest): Authenticated request.

        Returns:
            Response: List of user data.

        Raises:
            Exception: If query fails.
        """
        try:
            users = UserData.objects.all()
            serializer = UserSerializer(users, many=True)
            logger.info("User list fetched", count=len(users))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception("Error fetching user list", e, module_name=__name__)
            return Response(
                {"error": "Failed to retrieve user list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"], url_path="profile")
    @swagger_auto_schema(
        responses={
            200: openapi.Response("User data retrieved successfully"),
            401: openapi.Response("Authentication credentials were not provided."),
        },
        operation_description="Retrieve current user profile (requires authentication)",
    )
    def list_current_user(self, request):
        """
        Returns the current authenticated user's profile.

        Args:
            request (HttpRequest): Authenticated request.

        Returns:
            Response: Serialized user profile.
        """
        user = request.user
        logger.info("Fetching current user profile", user_id=user.id)
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLoginViewSet(SocialLoginView):
    """
    ViewSet for handling Google OAuth2 login.
    """
    adapter_class = GoogleOAuth2Adapter
