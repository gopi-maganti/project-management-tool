from rest_framework import serializers

from api.models import UserData


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
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

