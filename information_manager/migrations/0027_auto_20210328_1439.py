# Generated by Django 3.1.7 on 2021-03-28 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0026_auto_20210328_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('date_of_the_event',), 'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятия'},
        ),
    ]