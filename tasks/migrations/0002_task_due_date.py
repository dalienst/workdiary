# Generated by Django 5.0.6 on 2024-07-09 03:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
