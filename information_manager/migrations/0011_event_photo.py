# Generated by Django 3.1.7 on 2021-02-25 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0010_event_typeofevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.FileField(blank=True, upload_to='events/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
