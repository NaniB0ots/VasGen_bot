import telebot

from tg_admin_bot import models


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


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def is_authenticated(self):
        return self.chat_id in ['1234']

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