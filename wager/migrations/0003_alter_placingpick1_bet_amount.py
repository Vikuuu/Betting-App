# Generated by Django 5.0.7 on 2024-08-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wager', '0002_placingpick1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placingpick1',
            name='bet_amount',
            field=models.PositiveBigIntegerField(),
        ),
    ]
