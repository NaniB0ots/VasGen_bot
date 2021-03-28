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

    def send_message_to_all_users(self, text):
        pass

    def send_message_text_translation(self, match: information_manager_models.Event, text):
        """
        Отправка сообщения текстовой трансляции
        :param match:
        :param text:
        :return:
        """
        users = match.users_for_text_translation.all()
        title = 'Текстовая трансляция\n' \
                f'{match.title}\n' \
                f'----------------------------------\n\n'
        for user in users:
            self.send_message(chat_id=user.chat_id, text=title + text)

    def send_news(self, match: information_manager_models.News):
        pass


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.object = self._registration()

    def _registration(self):
        try:
            return models.TgUser.objects.get(chat_id=self.chat_id)
        except models.TgUser.DoesNotExist:
            return models.TgUser.objects.create(chat_id=self.chat_id)

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


class Match:
    def __init__(self, match_id):
        self.match_id = match_id
        self.object = self.get_queryset()

    def enable_match_notifications(self, chat_id):
        pass

    def disable_match_notifications(self, chat_id):
        pass

    def enable_text_translation(self, user: User):
        self.object.users_for_text_translation.add(user.object.id)

    def disable_text_translation(self, user: User):
        self.object.users_for_text_translation.remove(user.object.id)

    @staticmethod
    def get_matches_this_month() -> (str, list):
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                      'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        month_index = datetime.datetime.now().month
        month = month_list[month_index - 1]

        matches = information_manager_models.Event.objects.filter(type_of_event='match',
                                                                  date_of_the_event__month=month_index)
        return month, matches

    def get_queryset(self) -> information_manager_models.Event:
        try:
            return information_manager_models.Event.objects.get(id=self.match_id)
        except information_manager_models.Event.DoesNotExist:
            return None
