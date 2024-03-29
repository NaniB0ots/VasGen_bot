import telebot
import datetime

from tg_admin_bot import models
from information_manager import models as information_manager_models
from tg_bot.tg_bot import bot as tg_user_bot
from tg_admin_bot.utils import keyboards


class AdminBot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        text = 'Добрейшего времени суток, Админ!\n\n' \
               'Этот бот создан специально для Вас. ' \
               'Он поможет Вам с легкостью управлять ВАСГЕНом прямо с телефона: ' \
               'вести текстовую трансляцию во время матча и публиковать актуальные новости :)'

        return text

    @staticmethod
    def get_list_of_commands() -> str:
        text = '/start - запустить бота'

        return text

    @staticmethod
    def get_register_message():
        text = 'Для того чтобы начать пользоваться функциями бота, введите токен авторизации.\n\n ' \
               'Токен можно получить у администратора\n' \
               '@bolanebyla'
        return text

    @staticmethod
    def get_instruction() -> str:
        text = '<Инструкция по пользованию ботом...>'
        return text

    @staticmethod
    def get_authors() -> str:
        text = 'Авторы проекта ВасГен бот:\n' \
               'Сидоренко Анжелика - @alikastory\n' \
               'Лесков Алексей - @bolanebyla\n' \
               'Ашимов Султан - @ace_sultan\n'

        return text

    @staticmethod
    def get_error_text() -> str:
        text = 'Что-то пошло не так... Попробуйте ещё раз'
        return text

    def send_invalid_message_answer(self, chat_id):
        text = 'Я Вас не понимаю. Воспользуйтесь клавиатурой'
        self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_main_menu_keyboard())


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.object = self.get_object()

    def get_object(self):
        try:
            return models.TgAdminUser.objects.get(chat_id=self.chat_id)
        except models.TgAdminUser.DoesNotExist:
            models.TgAdminUser.objects.none()

    def is_authenticated(self):
        return self.get_object()

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
    def __init__(self, news_id: int = None, text: str = None, author: User = None):
        self.text = text
        self.news_id = news_id
        self.author = author
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
            return information_manager_models.News.objects.create(news=self.text, created_via_telegram=True,
                                                                  telegram_author=self.author.object)

    def send_news(self, photo):
        if self.object:
            tg_user_bot.send_news(news=self.object, photo=photo)
        else:
            ValueError('Объект новости не создан')

    @staticmethod
    def get_last_news() -> information_manager_models.News:
        return information_manager_models.News.objects.last()

    @staticmethod
    def delete_news(news_id):
        tg_user_bot.delete_sent_news(news_id=news_id)
