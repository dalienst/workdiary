# Generated by Django 5.0.6 on 2024-08-16 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_user_is_personal"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_finance",
            field=models.BooleanField(default=False),
        ),
    ]
