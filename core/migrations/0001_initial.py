# Generated by Django 5.0.6 on 2024-07-03 12:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("mobile", models.CharField(max_length=10, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("otp", models.IntegerField(max_length=6)),
                ("full_name", models.CharField(max_length=50)),
                ("dob", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        default="M",
                        max_length=1,
                    ),
                ),
                ("idNumber", models.CharField(max_length=50)),
                ("password", models.CharField(db_column="accountPin", max_length=4)),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["mobile"], name="core_userac_mobile_25d12f_idx"
                    )
                ],
            },
        ),
    ]
