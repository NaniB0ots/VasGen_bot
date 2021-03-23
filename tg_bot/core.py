import telebot
import datetime
from information_manager import models as information_manager_models
from tg_bot import models


class Bot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток!\n\n' \
                  'Тебя приветствует хоккейный помощник Иркутского политеха.\n' \
                  'Я расскажу тебе все о команде Иркутского политеха по хоккею с мячом, ' \
                  'подскажу раписание ближайших игр, а время игры буду вести текстовую трансляцию,' \
                  'еще с моей помощью можно приобрести билеты на матч и многое другое.\n\n' \
                  'Добро пожаловать!'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message


class Match:
    def enable_match_notifications(self, chat_id):
        pass

    def disable_match_notifications(self, chat_id):
        pass

    def enable_text_translation(self, chat_id):
        pass

    def disable_text_translation(self, chat_id):
        pass

    @staticmethod
    def get_matches_this_month() -> (str, list):
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                      'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        month_index = datetime.datetime.now().month
        month = month_list[month_index - 1]

        matches = information_manager_models.Event.objects.filter(type_of_event='match',
                                                                  date_of_the_event__month=month_index)
        return month, matches


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._registration()

    def _registration(self):
        try:
            models.TgUser.objects.get(chat_id=self.chat_id)
        except models.TgUser.DoesNotExist:
            models.TgUser.objects.create(chat_id=self.chat_id)

    def enable_match_notifications(self):
        pass

    def disable_match_notifications(self):
        pass

    def enable_newsletter(self):
        pass

    def disable_newsletter(self):
        pass


class BettingOnGames:
    def get_score(self, user: User) -> str:
        pass

    def get_matches_list(self) -> list:
        pass
