# Generated by Django 5.1.3 on 2024-12-27 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0014_resultmodel_total'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='description')),
                ('image', models.ImageField(upload_to='tasks/', verbose_name='banner')),
                ('file', models.FileField(blank=True, null=True, upload_to='tasks/', verbose_name='file')),
            ],
            options={
                'verbose_name': 'TaskModel',
                'verbose_name_plural': 'TaskModels',
                'db_table': 'task',
            },
        ),
        migrations.AddField(
            model_name='tutorialmodel',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorials', to='education.taskmodel', verbose_name='task'),
        ),
        migrations.CreateModel(
            name='TaskResultModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='taskresults/', verbose_name='file')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='education.taskmodel', verbose_name='task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'TaskresultModel',
                'verbose_name_plural': 'TaskresultModels',
                'db_table': 'taskresult',
            },
        ),
    ]
