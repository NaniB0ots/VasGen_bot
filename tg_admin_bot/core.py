import telebot
import datetime

from tg_admin_bot import models
from information_manager import models as information_manager_models
from tg_bot.tg_bot import bot as tg_user_bot


class AdminBot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток, Админ!\n\n' \
                  'Этот бот создан специально для Вас. ' \
                  'Он поможет Вам с легкостью управлять ВАСГЕНом прямо с телефона: ' \
                  'вести текстовую трансляцию во время матча и публиковать актуальные новости :)'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message

    @staticmethod
    def get_register_message():
        message = 'Для того чтобы начать пользоваться функциями бота, введите токен авторизации.\n\n ' \
                  'Токен можно получить у администратора\n' \
                  '@bolanebyla'
        return message

    @staticmethod
    def get_instruction() -> str:
        message = '<Инструкция по пользованию ботом...>'
        return message

    @staticmethod
    def get_authors() -> str:
        message = 'Авторы проекта ВасГен бот:\n' \
                  'Сидоренко Анжелика - @alikastory\n' \
                  'Лесков Алексей - @bolanebyla\n' \
                  'Ашимов Султан - @ace_sultan\n'

        return message

    @staticmethod
    def get_error_text() -> str:
        message = 'Что-то пошло не так... Попробуйте ещё раз'
        return message


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def is_authenticated(self):

        try:
            models.TgAdminUser.objects.get(chat_id=self.chat_id)
            return True
        except models.TgAdminUser.DoesNotExist:
            return False

    @staticmethod
    def authorization(chat_id, token, username):
        try:
            token_query = models.AdminUserToken.objects.get(token=token, is_used=False)
        except models.AdminUserToken.DoesNotExist:
            return None

        token_query.is_used = True
        token_query.save()

        user = models.TgAdminUser.objects.create(chat_id=chat_id, token=token_query, username=username)

        return user


class TextTranslation:
    def __init__(self, match_id):
        self.match_id = match_id
        self.match = information_manager_models.Event.objects.filter(type_of_event='match')
        self.object = self._get_match_query(match_id)

    @staticmethod
    def get_matches_of_the_day():
        day = datetime.datetime.now().day

        matches = information_manager_models.Event.objects.filter(type_of_event='match',
                                                                  date_of_the_event__day=day)
        return matches

    @staticmethod
    def _get_match_query(match_id):
        try:
            match_query = information_manager_models.Event.objects.get(id=match_id)
            return match_query
        except information_manager_models.Event.DoesNotExist:
            return None

    def send_text_translation_message(self, text):
        """
        Отправка сообщения текстовой трансляции
        :param text:
        :return:
        """
        tg_user_bot.send_message_text_translation(match=self.object, text=text)


class TgNews:
    def __init__(self, news_id: int = None, text: str = None):
        self.text = text
        self.news_id = news_id
        self.object = self.get_object()

    def get_object(self) -> information_manager_models.News:
        """
        Получение или создание объекта из базы данных
        :return:
        """
        if self.news_id:
            try:
                return information_manager_models.News.objects.get(id=self.news_id)
            except information_manager_models.News.DoesNotExist:
                information_manager_models.News.objects.none()
        elif self.text:
            return information_manager_models.News.objects.create(news=self.text, created_via_telegram=True)

    def send_news(self):
        pass
