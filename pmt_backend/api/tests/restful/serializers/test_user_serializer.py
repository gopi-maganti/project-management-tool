import pytest
from rest_framework.exceptions import ValidationError

from api.models import UserData
from api.restful.serializers.user_serializer import (
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


@pytest.mark.django_db
class TestUserRegisterSerializer:

    def test_valid_user_registration(self):
        data = {
            "username": "validuser",
            "email": "valid@gmail.com",
            "first_name": "Valid",
            "last_name": "User",
            "phone_number": "+1 (123) 456-7890",
            "password": "strongpass123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.username == data["username"]
        assert user.check_password(data["password"])

    def test_missing_required_fields(self):
        data = {"email": "no_username@gmail.com"}
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert "password" in serializer.errors

    def test_invalid_email_format(self):
        data = {
            "username": "emailfail",
            "email": "invalid-email",
            "first_name": "Email",
            "last_name": "Fail",
            "phone_number": "+1 (111) 222-3333",
            "password": "password123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_edge_case_short_username(self):
        data = {
            "username": "ab",  # less than 3 chars
            "email": "short@gmail.com",
            "first_name": "Short",
            "last_name": "Name",
            "phone_number": "+1 (111) 222-3333",
            "password": "edgecasepass",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_extra_field_ignored(self):
        data = {
            "username": "extrafield",
            "email": "extra@gmail.com",
            "first_name": "Extra",
            "last_name": "Field",
            "phone_number": "+1 (999) 999-9999",
            "password": "extra1234",
            "extra": "should_be_ignored",
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
class TestUserLoginSerializer:

    def test_valid_login(self):
        UserData.objects.create_user(
            username="testlogin", email="login@gmail.com", password="testpass"
        )
        data = {"username": "testlogin", "password": "testpass"}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["user"].username == "testlogin"

    def test_invalid_password(self):
        UserData.objects.create_user(
            username="wrongpass", email="fail@gmail.com", password="correctpass"
        )
        data = {"username": "wrongpass", "password": "wrongpass"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_missing_username(self):
        data = {"password": "somepass"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_nonexistent_user(self):
        data = {"username": "ghost", "password": "any"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestUserSerializer:

    def test_user_serializer_data(self):
        user = UserData.objects.create_user(
            username="viewme",
            email="view@gmail.com",
            password="viewpass",
            first_name="View",
            last_name="User",
            phone_number="+1 (555) 555-5555",
            is_admin=True,
        )
        serializer = UserSerializer(user)
        data = serializer.data
        assert data["username"] == "viewme"
        assert data["email"] == "view@gmail.com"
        assert data["is_admin"] is True
        assert "created_at" in data
        assert "modified_at" in data
