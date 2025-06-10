from rest_framework import serializers
from api.models import UserData

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserData
        fields = [
            "username", "email", "password",
            "first_name", "last_name", "phone_number"
        ]

    def create(self, validated_data):
        return UserData.objects.create_user(**validated_data)
