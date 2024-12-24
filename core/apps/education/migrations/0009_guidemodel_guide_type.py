# Generated by Django 5.1.3 on 2024-12-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_guidemodel_desc_guidemodel_file_guidemodel_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidemodel',
            name='guide_type',
            field=models.CharField(choices=[('superuser', 'Superuser'), ('admin', 'Admin'), ('user', 'User'), ('psixolog', 'Psixolog'), ('lawyer', 'Lawyer'), ('business', 'Business')], default=1, max_length=255, verbose_name='type'),
            preserve_default=False,
        ),
    ]
