# Generated by Django 3.1.7 on 2021-02-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0005_auto_20210225_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='goals_scored',
            field=models.IntegerField(default=0, verbose_name='Забитые голы'),
        ),
        migrations.AlterField(
            model_name='team',
            name='goals_scored',
            field=models.IntegerField(default=0, verbose_name='Забитые голы'),
        ),
    ]