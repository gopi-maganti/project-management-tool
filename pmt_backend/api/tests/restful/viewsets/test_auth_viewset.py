from typing import Any

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestAuthViewSet:
    def setup_method(self):
        self.client = APIClient()
    
    """
    Test cases for the AuthViewSet registration functionality.
    """
    def test_register_valid_user(self):
        response = self.client.post("/api/auth/register/", 
                                    {
                                        "username": "testuser2",
                                        "email": "test2@example.com",
                                        "first_name": "Test",
                                        "last_name": "User",
                                        "phone_number": "+1 (987) 654-3210",
                                        "password": "AnotherPass123!"
                                        },
                                    format="json")
        assert hasattr(response, "status_code"), f"Response object has no status_code attribute, got type: {type(response)}"
        assert getattr(response, "status_code", None) == 201, f"Expected status_code 201, got {getattr(response, 'status_code', None)} and type {type(response)}"
        assert "token" in getattr(response, "data", {}), f"Response data: {getattr(response, 'data', {})}"

    @pytest.mark.parametrize("payload, error_field", [
        # Missing email
        ({"username": "user1", "password": "pass1234"}, "email"),
        # Invalid email
        ({"username": "user2", "email": "invalid-email", "password": "pass1234"}, "email"),
        # Missing username
        ({"email": "user@example.com", "password": "pass1234"}, "username"),
        # Missing password
        ({"username": "user3", "email": "user3@example.com"}, "password"),
        # Invalid phone number format
        ({
            "username": "user4", "email": "user4@example.com", "password": "pass1234",
            "first_name": "User", "last_name": "Four", "phone_number": "1234567890"
        }, "phone_number"),
    ])
    def test_register_invalid_user(self, payload, error_field):
        response: Any = self.client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert error_field in response.data, f"Expected '{error_field}' error, got: {response.data}"

    
    def test_register_existing_user(self):
        response = self.client.post("/api/auth/register/", 
                                    {
                                        "username": "testuser2",
                                        "email": "test2@example.com",
                                        "first_name": "Test",
                                        "last_name": "User",
                                        "phone_number": "+1 (987) 654-3210",
                                        "password": "AnotherPass123!"
                                    },
                                    format="json")
        assert hasattr(response, "status_code"), f"Response object has no status_code attribute, got type: {type(response)}"
        assert getattr(response, "status_code", None) == 400, f"Expected status_code 400, got {getattr(response, 'status_code', None)} and type {type(response)}"
        assert "username" in getattr(response, "data", {}), f"Response data: {getattr(response, 'data', {})}"

    

    """
    Test cases for the AuthViewSet login functionality.
    """
    
    def test_login_valid_user(self):
        response = self.client.post("/api/auth/login/", {"username": "testuser", "password": "pass1234"}, format="json")
        assert hasattr(response, "status_code"), f"Response object has no status_code attribute, got type: {type(response)}"
        assert getattr(response, "status_code", None) == 200, f"Expected status_code 200, got {getattr(response, 'status_code', None)} and type {type(response)}"
        assert "token" in getattr(response, "data", {}), f"Response data: {getattr(response, 'data', {})}"

    def test_login_invalid_user(self):
        response = self.client.post("/api/auth/login/", {"username": "invaliduser", "password": "wrongpass"}, format="json")
        assert hasattr(response, "status_code"), f"Response object has no status_code attribute, got type: {type(response)}"
        assert getattr(response, "status_code", None) == 400, f"Expected status_code 400, got {getattr(response, 'status_code', None)} and type {type(response)}"
        assert "non_field_errors" in getattr(response, "data", {}), f"Response data: {getattr(response, 'data', {})}"