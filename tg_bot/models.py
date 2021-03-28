from django.db import models


class TgUser(models.Model):
    chat_id = models.IntegerField(unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    news_subscription = models.BooleanField(default=True, verbose_name='Подписка на новости')
    event_notifications = models.BooleanField(default=True, verbose_name='Подписка на мероприятия')

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'

    def __str__(self):
        return f'{self.chat_id}'
