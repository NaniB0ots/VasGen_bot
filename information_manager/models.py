from django.db import models

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
