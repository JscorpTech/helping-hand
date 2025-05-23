# Generated by Django 5.1.3 on 2024-12-17 09:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PositionModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name="location")),
            ],
            options={
                "verbose_name": "PositionModel",
                "verbose_name_plural": "PositionModels",
                "db_table": "position",
            },
        ),
    ]
