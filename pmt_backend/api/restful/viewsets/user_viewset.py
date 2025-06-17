from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from typing import cast
from api.restful.serializers.user_serializer import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for user registration functionality.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: UserRegisterSerializer, 400: "Bad Request"},
        operation_description="Register a new user."
    )
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.ViewSet):
    """
    Action to handle user login.
    Supports login via username/password or token.
    """
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
                        "access": "eyJhbGciOiJIUzI1NiIsIn...",
                        "user": {
                            "id": 1,
                            "username": "gopi",
                            "email": "gopi@example.com",
                            "first_name": "Gopi",
                            "last_name": "Kumar",
                            "phone_number": "+1 (123) 456-7890",
                            "is_admin": True
                        }
                    }
                }
            ),
            400: "Bad Request - Invalid credentials or input",
        },
        operation_description="User login with username/password. Returns JWT tokens and user info."
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = cast(dict, serializer.validated_data)
            user = authenticate(
                username=validated_data.get('username'),
                password=validated_data.get('password')
            )
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserRegisterSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login successful')},
        operation_description="Login with username and password"
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginViewSet(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
