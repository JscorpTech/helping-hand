# Generated by Django 5.1.3 on 2024-12-26 09:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0012_resultmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resultmodel',
            unique_together={('user', 'tutorial')},
        ),
    ]
