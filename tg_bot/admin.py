from django.contrib import admin

from tg_bot import models


@admin.register(models.TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'news_subscription', 'event_notifications')
    search_fields = ('chat_id',)
    list_filter = ('chat_id', 'news_subscription', 'event_notifications')
    ordering = ['-creation_date']
