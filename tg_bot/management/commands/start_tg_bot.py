from django.core.management.base import BaseCommand

from project.settings import DEBUG
from tg_bot.tg_bot import bot


class Command(BaseCommand):
    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        print('Бот запущен...')
        if DEBUG:
            bot.polling()
        else:
            bot.infinity_polling()
