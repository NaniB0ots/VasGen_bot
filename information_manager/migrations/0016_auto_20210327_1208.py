# Generated by Django 3.1.7 on 2021-03-27 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0015_auto_20210327_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]
