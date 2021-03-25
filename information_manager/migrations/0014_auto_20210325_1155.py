# Generated by Django 3.1.7 on 2021-03-25 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
        ('information_manager', '0013_auto_20210323_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='users_for_notifications',
            field=models.ManyToManyField(blank=True, to='tg_bot.TgUser', verbose_name='Пользователи для уведомлений'),
        ),
        migrations.AlterField(
            model_name='event',
            name='users_for_text_translation',
            field=models.ManyToManyField(blank=True, related_name='users_for_text_translation', to='tg_bot.TgUser', verbose_name='Пользователи для текстовой трансляции'),
        ),
    ]
