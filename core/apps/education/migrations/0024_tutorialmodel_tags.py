# Generated by Django 5.1.3 on 2025-01-08 08:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0023_remove_tutorialmodel_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tutorialmodel",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), blank=True, null=True, size=None, verbose_name="tags"
            ),
        ),
    ]
