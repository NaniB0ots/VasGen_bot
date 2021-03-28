import json

from project.settings import TG_TOKEN_ADMIN
from tg_admin_bot import core
from tg_admin_bot.core import AdminBot
from tg_admin_bot.utils import keyboards

if not TG_TOKEN_ADMIN:
    raise ValueError('TG_TOKEN_ADMIN не может быть пустым')

bot = AdminBot(TG_TOKEN_ADMIN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id, text=bot.get_start_message())

    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text=bot.get_instruction(), reply_markup=keyboards.get_main_menu_keyboard())


def authorization(message):
    chat_id = message.chat.id
    token = message.text
    username = message.from_user.username
    if core.User.authorization(chat_id=chat_id, token=token, username=username):
        bot.send_message(chat_id=chat_id, text=bot.get_instruction(), reply_markup=keyboards.get_main_menu_keyboard())
    else:
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)


@bot.message_handler(regexp='^Основное меню$')
def main_menu(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Основное меню',
                     reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(regexp='^Авторы')
def authors(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text=bot.get_authors())


@bot.message_handler(regexp='^Начать трансляцию$')
def text_translation(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return
    matches_queryset = core.TextTranslation.get_matches_of_the_day()
    if matches_queryset:
        bot.send_message(chat_id=chat_id,
                         text='Трансляцию какого матча Вы собираетесь вести?',
                         reply_markup=keyboards.get_inline_text_translation_matches_keyboard(matches_queryset))
    else:
        bot.send_message(chat_id=chat_id,
                         text='Сегодня матчей нет', reply_markup=keyboards.get_main_menu_keyboard())


@bot.callback_query_handler(func=lambda message: 'match' in message.data)
def text_translation_start(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    match_id = json.loads(message.data)['match']

    match = core.TextTranslation(match_id=match_id).object
    if match:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=match.title)
        msg = bot.send_message(chat_id=chat_id,
                               text='Окей! Запускаем вещание...\n'
                                    'Все, Вы в эфире.\n\n'
                                    'Для того, чтобы прекратить трансляцию, необходимо нажать на кнопку “Стоп”',
                               reply_markup=keyboards.get_stop_text_translation_keyboard())
        bot.register_next_step_handler(msg, translation, match_id=match_id)
    else:
        bot.send_message(chat_id=chat_id,
                         text=bot.get_error_text(),
                         reply_markup=keyboards.get_main_menu_keyboard())


def translation(message, match_id):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    text = message.text
    if text == 'Стоп':
        text_translation_stop(message)
        return

    match_translation = core.TextTranslation(match_id)
    match_translation.send_text_translation_message(text=text)
    msg = bot.send_message(chat_id=chat_id, text='Собщение отправлено')
    bot.register_next_step_handler(msg, translation, match_id=match_id)


@bot.message_handler(regexp='^Стоп$')
def text_translation_stop(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id,
                     text='Трансляция остановлена',
                     reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(regexp='^Новости$')
def news_menu(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Новости',
                     reply_markup=keyboards.get_news_keyboard())


@bot.message_handler(regexp='^Опубликовать новость$')
def write_news_start(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Для того, чтобы опубликовать новость, '
                                           'напишите текст новости в чат.\n\n'
                                           'Ждем вестей!',
                     reply_markup=keyboards.get_cancel_write_news_keyboard())

    msg = bot.send_message(chat_id=chat_id, text='ВАЖНО!\n'
                                                 'Пожалуйста, '
                                                 'Перед отправкой проверьте текст новости на наличие ошибок и опечаток.')

    bot.register_next_step_handler(msg, write_news)


def write_news(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    text = message.text

    news = core.TgNews(text=text)
    if news.object:
        news.send_news()
        bot.send_message(chat_id=chat_id, text='Новость успшно отправлена')
    else:
        bot.send_message(chat_id=chat_id, text=bot.get_error_text())


@bot.message_handler(regexp='^Отмена$')
def write_news_cancel(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Отмена',
                     reply_markup=keyboards.get_news_keyboard())
