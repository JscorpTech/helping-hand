# Generated by Django 5.1.5 on 2025-01-28 13:47


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0003_userrequestmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequestmodel',
            name='area',
            field=models.CharField(choices=[('unsafe', 'Xafli hudud'), ('safe', 'Xafsiz hudud')], max_length=255, verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='userrequestmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sos_requests', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
