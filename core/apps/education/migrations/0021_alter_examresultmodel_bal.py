# Generated by Django 5.1.3 on 2024-12-28 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0020_exammodel_examresultmodel_sertificatemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresultmodel',
            name='bal',
            field=models.IntegerField(default=0),
        ),
    ]
