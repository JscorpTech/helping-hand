# Generated by Django 5.1.3 on 2025-01-16 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0026_remove_questionmodel_file_delete_answermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidemodel',
            name='desc_kaa',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='guidemodel',
            name='desc_kril',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='guidemodel',
            name='desc_uz',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='guidemodel',
            name='name_kaa',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='guidemodel',
            name='name_kril',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='guidemodel',
            name='name_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='question_kaa',
            field=models.TextField(null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='question_kril',
            field=models.TextField(null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='question_uz',
            field=models.TextField(null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='desc_kaa',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='desc_kril',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='desc_uz',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='topic_kaa',
            field=models.CharField(max_length=255, null=True, verbose_name='topic'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='topic_kril',
            field=models.CharField(max_length=255, null=True, verbose_name='topic'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='topic_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='topic'),
        ),
        migrations.AddField(
            model_name='variantmodel',
            name='variant_kaa',
            field=models.CharField(max_length=255, null=True, verbose_name='variant'),
        ),
        migrations.AddField(
            model_name='variantmodel',
            name='variant_kril',
            field=models.CharField(max_length=255, null=True, verbose_name='variant'),
        ),
        migrations.AddField(
            model_name='variantmodel',
            name='variant_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='variant'),
        ),
    ]
