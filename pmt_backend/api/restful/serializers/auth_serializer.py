from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.constants import LOGIN_TYPE_CHOICES
from api.models import UserData


class LoginTypeSerializer(serializers.Serializer):

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