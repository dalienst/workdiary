# Generated by Django 5.0.6 on 2024-08-14 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0002_company_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
