from django.db import models


class AdminUserToken(models.Model):
    token = models.CharField(max_length=8)
    is_used = models.BooleanField(default=False, verbose_name='Ипользовано')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')

    class Meta:
        verbose_name = 'Токен администратора'
        verbose_name_plural = 'Токены администраторов'

    def __str__(self):
        return f'{self.token}'


class TgAdminUser(models.Model):
    chat_id = models.IntegerField()
    username = models.CharField(max_length=60)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    token = models.OneToOneField(AdminUserToken, verbose_name='Токен регистрации', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Телеграм админ'
        verbose_name_plural = 'Телеграм админ'

    def __str__(self):
        return f'{self.chat_id}'


class AdminNews(models.Model):
    text = models.TextField(verbose_name='Текст новости')
    message_id = models.IntegerField()

    class Meta:
        verbose_name = 'Новость созданная через телеграм'
        verbose_name_plural = 'Новость созданная через телеграм'

    def __str__(self):
        return f'{self.text[:50]}'
