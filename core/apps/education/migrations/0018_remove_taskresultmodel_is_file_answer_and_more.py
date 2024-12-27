# Generated by Django 5.1.3 on 2024-12-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0017_taskresultmodel_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskresultmodel',
            name='is_file_answer',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='is_file_answer',
            field=models.BooleanField(default=False, verbose_name='is answer file'),
        ),
    ]