from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from api.models import UserData
from api.restful.serializers import UserRegisterSerializer, LoginSerializer
from api.utils.auth import auth_required  # Custom Auth0-based decorator


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for user registration, login, and restricted user listing.
    """

    @swagger_auto_schema(
        method='post',
        request_body=UserRegisterSerializer,
        responses={201: openapi.Response('User registered successfully')}
    )
    @action(detail=False, methods=['post'], url_path='register')
    @auth_required
    def register(self, request):
        # Extract creator's role from the JWT token
        creator_role = request.user_payload.get("role", "").lower()
        
        # Extract target role from request body
        target_role = request.data.get("role", "").lower()

        # Authorization logic
        if target_role == "admin" and creator_role not in ["superuser", "admin"]:
            return Response({"error": "Only superusers or admins can create admins"}, status=status.HTTP_403_FORBIDDEN)
        elif target_role == "employee" and creator_role not in ["superuser", "admin"]:
            return Response({"error": "Only superusers or admins can create employees"}, status=status.HTTP_403_FORBIDDEN)

        # Continue with registration
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": f"{target_role.capitalize()} registered successfully",
                "token": token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Auth Token')
                }
            )),
            401: 'Invalid credentials'
        }
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your_token>",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                'List of users (admin/superuser only)',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        }
                    )
                )
            ),
            403: 'Forbidden – not authorized via token'
        }
    )
    @action(detail=False, methods=['get'], url_path='list')
    @auth_required
    def list_users(self, request):
        payload = request.user_payload

        # You can inspect payload like this:
        user_email = payload.get("email")
        user_id = payload.get("sub")  # Auth0 user ID (like auth0|abc123)
        permissions = payload.get("permissions", [])

        # Example permission check
        if "read:admin_users" not in permissions:
            return Response({"detail": "Access denied. Missing permission: read:admin_users"}, status=403)

        users = UserData.objects.all().values(
            "id", "username", "email", "first_name", "last_name", "phone_number", "is_admin", "is_superuser"
        )
        return Response(users, status=status.HTTP_200_OK)
