# Generated by Django 5.1.3 on 2024-12-16 13:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0007_groupmodel_chat_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="groupmodel",
            index=models.Index(fields=["name"], name="group_name_9aba6c_idx"),
        ),
        migrations.AddIndex(
            model_name="groupmodel",
            index=models.Index(fields=["chat_type"], name="group_chat_ty_7e3843_idx"),
        ),
    ]
