# Generated by Django 3.1.7 on 2021-03-27 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_manager', '0016_auto_20210327_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachingStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=80, verbose_name='Фамилия')),
                ('firstname', models.CharField(max_length=80, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=80, verbose_name='Отчество')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('photo', models.FileField(blank=True, upload_to='players/', verbose_name='Фото')),
                ('post', models.CharField(blank=True, max_length=80, verbose_name='Должность')),
                ('brief_information', models.TextField(blank=True, verbose_name='Краткая информация')),
                ('progress', models.TextField(blank=True, verbose_name='Достижения (карьера)')),
                ('wins', models.IntegerField(blank=True, verbose_name='Победы')),
                ('losses', models.IntegerField(blank=True, verbose_name='Поражения')),
                ('goals_scored', models.IntegerField(blank=True, verbose_name='Голы')),
                ('goalscoring_matches', models.IntegerField(blank=True, verbose_name='Голевые матчи')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Тренерский штаб',
                'verbose_name_plural': 'Тренерский штаб',
                'ordering': ('lastname', 'firstname'),
            },
        ),
        migrations.AlterField(
            model_name='player',
            name='assists',
            field=models.IntegerField(blank=True, verbose_name='Голевые передачи'),
        ),
        migrations.AlterField(
            model_name='player',
            name='firstname',
            field=models.CharField(max_length=80, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='player',
            name='goals_scored',
            field=models.IntegerField(blank=True, verbose_name='Забитые голы'),
        ),
        migrations.AlterField(
            model_name='player',
            name='lastname',
            field=models.CharField(max_length=80, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='player',
            name='losses',
            field=models.IntegerField(blank=True, verbose_name='Поражения'),
        ),
        migrations.AlterField(
            model_name='player',
            name='patronymic',
            field=models.CharField(blank=True, max_length=80, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='player',
            name='playing_position',
            field=models.CharField(blank=True, max_length=80, verbose_name='Амплуа'),
        ),
        migrations.AlterField(
            model_name='player',
            name='wins',
            field=models.IntegerField(blank=True, verbose_name='Победы'),
        ),
    ]
