from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import UserData


class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Username or Email")
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        user = UserData.objects.filter(email=identifier).first() or UserData.objects.filter(username=identifier).first()
        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
        raise serializers.ValidationError("Invalid credentials")
