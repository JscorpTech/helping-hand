# Generated by Django 5.1.3 on 2025-01-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_user_auth_provider_alter_user_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="moderatormodel",
            name="level",
            field=models.CharField(default=1),
        ),
    ]
