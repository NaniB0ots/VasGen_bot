from django.contrib import admin

from information_manager import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title', 'educational_institution')
    search_fields = ('title', 'educational_institution',)
    ordering = ['-update_date']


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'patronymic', 'playing_position', 'is_captain',)
    search_fields = ('lastname', 'firstname', 'patronymic', 'is_captain', 'playing_position',)
    list_filter = ('is_captain', 'playing_position')
    ordering = ['lastname', 'firstname']


@admin.register(models.CoachingStaff)
class CoachingStaffAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'patronymic', 'post',)
    search_fields = ('lastname', 'firstname', 'patronymic', 'post',)
    list_filter = ('post',)
    ordering = ['lastname', 'firstname']


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_of_the_event', 'type_of_event')
    search_fields = ('title', 'description', 'date_of_the_event')
    ordering = ['-update_date']


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news', 'creation_date', 'author', 'created_via_telegram', 'telegram_author',)
    search_fields = ('title', 'news',)
    list_filter = ('author',)


@admin.register(models.SentNews)
class SentNewsAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'message_id')
