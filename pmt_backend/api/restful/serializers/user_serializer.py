from rest_framework import serializers

from api.models import UserData
from api.constants import LOGIN_TYPE_CHOICES


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
        extra_kwargs = {"username": {"required": True, "max_length": 150, "min_length": 3},
                        "email": {"required": True, "max_length": 254, "min_length": 5},
                        "password": {"write_only": True}, 
                        "is_admin": {"required": False, "default": False}}

    def create(self, validated_data):
        user = UserData.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login with different methods.
    Supports username/password, token, and Google SSO.
    """
    login_type = serializers.ChoiceField(choices=LOGIN_TYPE_CHOICES)

    # Fields used for username/password login
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    # Token login
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        login_type = attrs.get("login_type")

        if login_type == "username_password":
            if not attrs.get("username") or not attrs.get("password"):
                raise serializers.ValidationError("Username and password are required.")
        elif login_type == "token":
            if not attrs.get("token"):
                raise serializers.ValidationError("Token is required.")
        elif login_type == "google":
            # For Google SSO, frontend typically redirects with social token or auth code.
            pass
        else:
            raise serializers.ValidationError("Invalid login type.")

        return attrs