from rest_framework import serializers
from api.models import UserData

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserData.objects.create_user(**validated_data)
        return user
