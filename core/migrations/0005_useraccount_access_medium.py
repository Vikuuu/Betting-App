# Generated by Django 5.0.6 on 2024-07-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_useraccount_otp_verified"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="access_medium",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
