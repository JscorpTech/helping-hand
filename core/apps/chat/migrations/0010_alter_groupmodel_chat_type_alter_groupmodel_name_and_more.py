# Generated by Django 5.1.3 on 2025-01-10 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0009_messagemodel_file_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupmodel",
            name="chat_type",
            field=models.CharField(
                blank=True,
                choices=[("lawyer", "Lawyer"), ("psixolog", "Psixolog"), ("business", "Business")],
                null=True,
                verbose_name="chat type",
            ),
        ),
        migrations.AlterField(
            model_name="groupmodel",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="messagemodel",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="chat.groupmodel",
                verbose_name="group",
            ),
        ),
    ]
