from django.db import models

from tg_bot.models import TgUser
from user_profile.models import Profile


class Tag(models.Model):
    tag = models.CharField(max_length=30, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.tag}'


class News(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название')
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    news = models.TextField(verbose_name='Текст новости')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    photo = models.FileField(verbose_name='Фото', upload_to='news/%Y/%m/%d/', blank=True)
    source = models.URLField(verbose_name='Источник', blank=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.title}'


class Team(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=25, verbose_name='Название')
    educational_institution = models.CharField(max_length=40, verbose_name='Учебное заведение')

    wins = models.IntegerField(default=0, verbose_name='Победы')
    losses = models.IntegerField(default=0, verbose_name='Поражения')
    goals_scored = models.IntegerField(default=0, verbose_name='Забитые голы')
    games_in_the_season = models.IntegerField(default=0, verbose_name='Игры в сезоне')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return f'{self.title}'


class Player(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    lastname = models.CharField(max_length=25, verbose_name='Фамилия')
    firstname = models.CharField(max_length=25, verbose_name='Имя')
    patronymic = models.CharField(max_length=25, verbose_name='Отчество', blank=True)
    age = models.IntegerField(verbose_name='Возраст', blank=True)
    photo = models.FileField(verbose_name='Фото', upload_to='players/', blank=True)
    team = models.ForeignKey(Team, verbose_name='Команда', blank=True, null=True, on_delete=models.SET_NULL)
    playing_position = models.CharField(max_length=25, verbose_name='Позиция', blank=True)
    is_captain = models.BooleanField(default=False, verbose_name='Капитан')

    wins = models.IntegerField(default=0, verbose_name='Победы')
    losses = models.IntegerField(default=0, verbose_name='Поражения')
    goals_scored = models.IntegerField(default=0, verbose_name='Забитые голы')
    games_in_the_season = models.IntegerField(default=0, verbose_name='Игры в сезоне')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Event(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=60, verbose_name='Название')
    date_of_the_event = models.DateTimeField(blank=True, verbose_name='Дата мероприятия')
    type_of_event = models.CharField(choices=[('match', 'матч')], max_length=150, verbose_name='Тип мероприятия',
                                     blank=True)
    description = models.CharField(max_length=200, verbose_name='Описание')
    photo = models.FileField(verbose_name='Фото', upload_to='events/%Y/%m/%d/', blank=True)
    teams = models.ManyToManyField(Team, blank=True, verbose_name='Команды')

    users_for_notifications = models.ManyToManyField(TgUser, verbose_name='Пользователи для уведомлений')
    users_for_text_translation = models.ManyToManyField(TgUser, related_name='users_for_text_translation',
                                                        verbose_name='Пользователи для текстовой трансляции')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return f'{self.title}'
