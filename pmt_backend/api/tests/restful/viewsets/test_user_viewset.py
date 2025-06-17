import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import UserData


@pytest.mark.django_db
class TestUserViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.register_url = "/api/user/register/"
        self.login_token_url = "/api/user/token/"
        self.login_jwt_url = "/api/user/login/"
        self.list_url = "/api/user/list/"
        self.profile_url = "/api/user/profile/"

    # ----------------- REGISTER -----------------
    def test_register_valid_user(self):
        payload = {
            "username": "testuser",
            "email": "test@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1 (123) 456-7890",
            "password": "testpass123",
            "is_admin": False,
        }
        response = self.client.post(self.register_url, payload, format="json")
        assert response.status_code == 201
        assert "token" in response.data
        assert response.data["user"]["username"] == "testuser"

    def test_register_missing_fields(self):
        response = self.client.post(
            self.register_url, {"email": "incomplete@gmail.com"}, format="json"
        )
        assert response.status_code == 400
        assert "username" in response.data
        assert "password" in response.data

    # ----------------- TOKEN LOGIN -----------------
    def test_login_token_success(self):
        UserData.objects.create_user(
            username="loguser", email="log@gmail.com", password="logpass"
        )
        response = self.client.post(
            self.login_token_url, {"username": "loguser", "password": "logpass"}
        )
        assert response.status_code == 200
        assert "token" in response.data
        assert response.data["user"]["username"] == "loguser"

    def test_login_token_invalid_credentials(self):
        response = self.client.post(
            self.login_token_url, {"username": "ghost", "password": "wrongpass"}
        )
        assert response.status_code == 401
        assert "error" in response.data

    # ----------------- JWT LOGIN -----------------
    def test_login_jwt_success(self):
        UserData.objects.create_user(
            username="jwtuser", email="jwt@gmail.com", password="jwtpass"
        )
        response = self.client.post(
            self.login_jwt_url, {"username": "jwtuser", "password": "jwtpass"}
        )
        assert response.status_code == 200
        assert "access" in response.data and "refresh" in response.data

    def test_login_jwt_invalid(self):
        response = self.client.post(
            self.login_jwt_url, {"username": "fake", "password": "wrong"}
        )
        assert response.status_code == 400

    # ----------------- USER LIST -----------------
    def test_user_list_authenticated(self):
        user = UserData.objects.create_user(
            username="listuser", email="list@gmail.com", password="listpass"
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(self.list_url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_user_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        assert response.status_code == 401

    # ----------------- CURRENT USER PROFILE -----------------
    def test_current_user_profile_authenticated(self):
        user = UserData.objects.create_user(
            username="me", email="me@gmail.com", password="mypass"
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(self.profile_url)
        assert response.status_code == 200
        assert response.data["username"] == "me"

    def test_current_user_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        assert response.status_code == 401
