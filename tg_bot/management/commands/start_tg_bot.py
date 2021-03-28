from django.core.management.base import BaseCommand
from threading import Thread
from project.settings import DEBUG
from tg_bot.tg_bot import bot


class Command(BaseCommand):
    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        # запуск напоминаний
        start_reminders = Thread(target=bot.start_reminders)
        start_reminders.start()

        print('Бот запущен...')
        if DEBUG:
            bot.polling()
        else:
            bot.infinity_polling()
