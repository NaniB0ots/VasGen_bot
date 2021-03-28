# Generated by Django 3.1.7 on 2021-03-27 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0022_auto_20210327_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentnews',
            name='created_via_telegram',
        ),
        migrations.AddField(
            model_name='news',
            name='created_via_telegram',
            field=models.BooleanField(default=False, verbose_name='Создано через телеграм'),
        ),
    ]
