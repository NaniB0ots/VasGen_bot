# Generated by Django 3.1.7 on 2021-02-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0002_auto_20210222_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.FileField(blank=True, upload_to='news/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
