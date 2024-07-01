# Generated by Django 5.0.6 on 2024-07-01 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0002_invoiceitem"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="status",
        ),
        migrations.AddField(
            model_name="invoice",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
    ]
