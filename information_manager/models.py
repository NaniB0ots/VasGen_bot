from django.db import models

from tg_bot.models import TgUser
from tg_admin_bot.models import TgAdminUser
from user_profile.models import Profile


class News(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название', blank=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    news = models.TextField(verbose_name='Текст новости')

    photo = models.FileField(verbose_name='Фото', upload_to='news/%Y/%m/%d/', blank=True)
    source = models.URLField(verbose_name='Источник', blank=True)

    created_via_telegram = models.BooleanField(default=False, verbose_name='Создано через телеграм')
    telegram_author = models.ForeignKey(TgAdminUser, on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name='Телеграм автор')

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.title if self.title else self.news}'


class SentNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость', )
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, verbose_name='Телеграм пользователь')
    message_id = models.IntegerField()

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отправленная новость'
        verbose_name_plural = 'Отправленные новости'
        ordering = ('-update_date',)

    def __str__(self):
        return f'{self.news}'


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
    lastname = models.CharField(max_length=80, verbose_name='Фамилия')
    firstname = models.CharField(max_length=80, verbose_name='Имя')
    patronymic = models.CharField(max_length=80, verbose_name='Отчество', blank=True)
    birthdate = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    photo = models.FileField(verbose_name='Фото', upload_to='players/', blank=True)

    playing_position = models.CharField(max_length=80, verbose_name='Амплуа', blank=True)
    is_captain = models.BooleanField(default=False, verbose_name='Капитан')

    brief_information = models.TextField(verbose_name='Краткая информация', blank=True)
    progress = models.TextField(verbose_name='Достижения (карьера)', blank=True)

    number_of_matches = models.IntegerField(verbose_name='Количество матчей', blank=True, null=True)
    goals_scored = models.IntegerField(verbose_name='Забитые голы', blank=True, null=True)
    assists = models.IntegerField(verbose_name='Голевые передачи', blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ('lastname', 'firstname')

    def __str__(self):
        return f'{self.lastname} {self.firstname}'


class CoachingStaff(models.Model):
    lastname = models.CharField(max_length=80, verbose_name='Фамилия')
    firstname = models.CharField(max_length=80, verbose_name='Имя')
    patronymic = models.CharField(max_length=80, verbose_name='Отчество', blank=True)
    birthdate = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    photo = models.FileField(verbose_name='Фото', upload_to='players/', blank=True)

    post = models.CharField(max_length=80, verbose_name='Должность', blank=True)

    brief_information = models.TextField(verbose_name='Краткая информация', blank=True)
    progress = models.TextField(verbose_name='Достижения (карьера)', blank=True)

    number_of_matches = models.IntegerField(verbose_name='Количество матчей', blank=True, null=True)
    goals_scored = models.IntegerField(verbose_name='Голы', blank=True, null=True)
    assists = models.IntegerField(verbose_name='Голевые передачи', blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Тренерский штаб'
        verbose_name_plural = 'Тренерский штаб'
        ordering = ('lastname', 'firstname')

    def __str__(self):
        return f'{self.lastname} {self.firstname}'


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

    users_for_notifications = models.ManyToManyField(TgUser, blank=True, verbose_name='Пользователи для уведомлений')
    users_for_text_translation = models.ManyToManyField(TgUser, blank=True, related_name='users_for_text_translation',
                                                        verbose_name='Пользователи для текстовой трансляции')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ('date_of_the_event',)

    def __str__(self):
        return f'{self.title}'
