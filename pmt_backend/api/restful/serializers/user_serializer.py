import structlog
from rest_framework import serializers

from api.models import UserData

logger = structlog.get_logger().bind(module='user_serializer')

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including fields for username, email, first name, last name,
    phone number, password, and admin status.
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

    def create(self, validated_data):
        logger.info("Creating user", validated_data={k: v for k, v in validated_data.items() if k != "password"})
        try:
            user = UserData.objects.create_user(**validated_data)
            logger.info("User created successfully", user_id=user.id)
            return user
        except Exception as e:
            logger.error("Error creating user", error=str(e))
            raise serializers.ValidationError("User creation failed. Please check the data provided.")


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login with different methods.
    Supports username/password, token, and Google SSO.
    """

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
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
    Serializer for user data, including fields for username, email, first name, last name,
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
