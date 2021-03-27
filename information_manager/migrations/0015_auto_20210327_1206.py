# Generated by Django 3.1.7 on 2021-03-27 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0014_auto_20210325_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('lastname', 'firstname'), 'verbose_name': 'Игрок', 'verbose_name_plural': 'Игроки'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='age',
        ),
        migrations.RemoveField(
            model_name='player',
            name='games_in_the_season',
        ),
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AddField(
            model_name='player',
            name='assists',
            field=models.IntegerField(default=0, verbose_name='Голевые передачи'),
        ),
        migrations.AddField(
            model_name='player',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='player',
            name='brief_information',
            field=models.TextField(blank=True, verbose_name='Краткая информация'),
        ),
        migrations.AddField(
            model_name='player',
            name='progress',
            field=models.TextField(blank=True, verbose_name='Достижения (карьера)'),
        ),
        migrations.AlterField(
            model_name='player',
            name='playing_position',
            field=models.CharField(blank=True, max_length=25, verbose_name='Амплуа'),
        ),
    ]