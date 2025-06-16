from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserData(AbstractUser):
    """
    This model represents a user in the system with custom fields.
    """

    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Unique username for the user",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.-]+$",
                message="Username must contain only letters, numbers, underscores, or hyphens.",
            )
        ],
    )
    first_name = models.CharField(max_length=150, help_text="First Name of the user")
    last_name = models.CharField(max_length=150, help_text="Last Name of the user")
    phone_number = models.CharField(
        max_length=17,
        help_text="Phone Number of the user, e.g., +1 (XXX) XXX-XXXX",
        validators=[
            RegexValidator(
                regex=r"^\+1 \(\d{3}\) \d{3}-\d{4}$",
                message="Phone number must be in the format: +1 (XXX) XXX-XXXX",
            )
        ],
    )
    email = models.CharField(
        max_length=254,
        help_text="Email Address of the user",
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w\.-]+@[\w\.-]+\.\w+$",
                message="Enter a valid email address (e.g., xyz@zyx.com)",
            )
        ],
    )
    is_admin = models.BooleanField(
        default=False, help_text="Marks whether the user has admin privileges."
    )
    is_active = models.BooleanField(
        default=True, help_text="Designates whether this user account is active."
    )
    created_at = models.DateTimeField(
        default=timezone.now, editable=False, help_text="User creation timestamp."
    )
    modified_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of the last modification."
    )
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
        help_text="User who created this account.",
    )

    # Prevent related_name conflicts with default groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username
