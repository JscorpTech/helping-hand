# Generated by Django 5.1.3 on 2025-01-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='is_top',
            field=models.BooleanField(default=False, verbose_name='is top'),
        ),
    ]
