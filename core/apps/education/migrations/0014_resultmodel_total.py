# Generated by Django 5.1.3 on 2024-12-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_alter_resultmodel_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultmodel',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='total'),
        ),
    ]
