# Generated by Django 3.1.7 on 2021-03-28 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='chat_id',
            field=models.IntegerField(unique=True),
        ),
    ]
