from django.contrib import admin

from information_manager import models


@admin.register(models.News)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'news',)
    list_filter = ('author', 'tags')
    ordering = ['-update_date']


admin.site.register(models.Tag)
