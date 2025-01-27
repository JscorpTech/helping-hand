# Generated by Django 5.1.5 on 2025-01-27 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0008_alter_notificationmodel_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqcategorymodel',
            options={'verbose_name': 'FaqCategoryModel', 'verbose_name_plural': 'FaqCategoryModels'},
        ),
        migrations.AddField(
            model_name='faqcategorymodel',
            name='name_kaa',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='faqcategorymodel',
            name='name_kril',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='faqcategorymodel',
            name='name_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='answer_kaa',
            field=models.TextField(null=True, verbose_name='answer'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='answer_kril',
            field=models.TextField(null=True, verbose_name='answer'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='answer_uz',
            field=models.TextField(null=True, verbose_name='answer'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='question_kaa',
            field=models.TextField(null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='question_kril',
            field=models.TextField(null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='faqmodel',
            name='question_uz',
            field=models.TextField(null=True, verbose_name='question'),
        ),
    ]
