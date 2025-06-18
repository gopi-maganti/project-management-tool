import pytest
from django.core.exceptions import ValidationError

from api.models import UserData


@pytest.mark.django_db
class TestUserDataModel:

    def test_create_valid_user(self):
        user = UserData.objects.create_user(
            username="valid_user1",
            email="valid@gmail.com",
            password="strongpass123",
            first_name="Valid",
            last_name="User",
            phone_number="+1 (123) 456-7890",
        )
        assert user.pk is not None
        assert user.check_password("strongpass123")

    @pytest.mark.parametrize(
        "field, value, expected_error",
        [
            ("username", "invalid#name", "Username must contain only letters"),
            ("email", "user@yahoo.com", "Enter a valid email address"),
            ("phone_number", "1234567890", "Phone number must be in the format"),
        ],
    )
    def test_invalid_fields(self, field, value, expected_error):
        valid_data = {
            "username": "validuser",
            "email": "valid@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1 (123) 456-7890",
        }

        # Replace the specific field with an invalid value
        valid_data[field] = value

        user = UserData(**valid_data)
        with pytest.raises(ValidationError) as exc:
            user.full_clean()

        assert expected_error in str(exc.value)
