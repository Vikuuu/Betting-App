# Generated by Django 5.0.6 on 2024-07-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_useraccount_access_medium"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="otp",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
