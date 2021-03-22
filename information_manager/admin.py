from django.contrib import admin

from information_manager import models


@admin.register(models.News)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'news',)
    list_filter = ('author', 'tags')
    ordering = ['-update_date']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title', 'educational_institution')
    search_fields = ('title', 'educational_institution',)
    ordering = ['-update_date']


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'team', 'playing_position')
    search_fields = ('firstname', 'lastname', 'team', 'playing_position', 'patronymic', 'age')
    list_filter = ('is_captain', 'team')
    ordering = ['-update_date']


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_of_the_event', 'type_of_event')
    search_fields = ('title', 'description', 'date_of_the_event')
    ordering = ['-update_date']
