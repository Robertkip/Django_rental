# Generated by Django 5.0.7 on 2024-08-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0004_alter_transaction_reference_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
