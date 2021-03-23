from django.core.management.base import BaseCommand

from project.settings import DEBUG
from tg_admin_bot.tg_admin_bot import bot


class Command(BaseCommand):
    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        print('Админ бот запущен...')
        if DEBUG:
            bot.polling()
        else:
            bot.infinity_polling()
