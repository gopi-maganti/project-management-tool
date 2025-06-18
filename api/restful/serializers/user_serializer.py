from typing import Any, Dict
import structlog
from rest_framework import serializers
from api.models import UserData

logger = structlog.get_logger().bind(module='user_serializer')

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of new users with required fields such as username, email,
    first name, last name, phone number, password, and admin status.

    Raises:
        ValidationError: If user creation fails internally.
    """

    class Meta:
        model = UserData
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "is_admin",
        )
        extra_kwargs = {
            "username": {"required": True, "max_length": 150, "min_length": 3},
            "email": {"required": True, "max_length": 254, "min_length": 5},
            "password": {"write_only": True},
            "is_admin": {"required": False, "default": False},
        }

    def create(self, validated_data: Dict[str, Any]) -> UserData:
        """
        Creates and returns a new User instance.

        Args:
            validated_data (dict): Validated data for creating the user.

        Returns:
            UserData: The created user instance.

        Raises:
            ValidationError: If an error occurs during user creation.
        """
        try:
            user = UserData.objects.create_user(**validated_data)
            return user
        except Exception as e:
            logger.error("Error creating user", error=str(e))
            raise serializers.ValidationError("User creation failed. Please check the data provided.")


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login.

    Supports username/password-based authentication and validates user credentials.

    Raises:
        ValidationError: If credentials are missing or incorrect.
    """

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the provided username and password.

        Args:
            attrs (dict): Dictionary with 'username' and 'password'.

        Returns:
            dict: Validated data with user instance.

        Raises:
            ValidationError: If user does not exist or password is incorrect.
        """
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = UserData.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing user data.

    Returns detailed information such as ID, username, email, first and last name,
    phone number, admin status, and timestamps.
    """

    class Meta:
        model = UserData
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_admin",
            "created_at",
            "modified_at",
        )
        read_only_fields = ("id", "created_at", "modified_at")
