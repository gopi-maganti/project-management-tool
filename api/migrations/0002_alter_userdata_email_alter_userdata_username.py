# Generated by Django 5.2.2 on 2025-06-17 02:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdata",
            name="email",
            field=models.CharField(
                help_text="Email Address of the user",
                max_length=254,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Enter a valid email address (e.g., xyz@gmail.com)",
                        regex="^[\\w\\.-]+@gmail\\.com$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="userdata",
            name="username",
            field=models.CharField(
                help_text="Unique username for the user",
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Username must contain only letters, numbers, underscores, or hyphens.",
                        regex="^[a-zA-Z0-9_.-]+$",
                    )
                ],
            ),
        ),
    ]
