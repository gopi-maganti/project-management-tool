import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
                                        username="testuser2",
                                        email="test2@example.com",
                                        first_name="Test",
                                        last_name="User",
                                        phone_number="+1 (987) 654-3210",
                                        password="AnotherPass123!"
                                    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.check_password("pass123")

@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
    assert admin.is_superuser
    assert admin.is_staff
