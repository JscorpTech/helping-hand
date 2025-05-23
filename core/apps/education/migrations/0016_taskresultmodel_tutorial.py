# Generated by Django 5.1.3 on 2024-12-27 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0015_taskmodel_tutorialmodel_task_taskresultmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskresultmodel",
            name="tutorial",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="taskresults",
                to="education.tutorialmodel",
                verbose_name="tutorial",
            ),
            preserve_default=False,
        ),
    ]
