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
    bot.send_message(chat_id=chat_id, text='Отправка...')
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
    if text == 'Отмена':
        write_news_cancel(message)
        return

    photo = None
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        photo = bot.download_file(file_info.file_path)
        text = message.caption

    news = core.TgNews(text=text, author=user)
    if news.object:
        bot.send_message(chat_id=chat_id, text='Отправка...')
        news.send_news(photo=photo)
        bot.send_message(chat_id=chat_id, text='Новость успшно отправлена',
                         reply_markup=keyboards.get_main_menu_keyboard())
    else:
        bot.send_message(chat_id=chat_id, text=bot.get_error_text(), reply_markup=keyboards.get_news_keyboard())


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


@bot.message_handler(regexp='^Удалить последнюю новость$')
def delete_last_news(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    last_news = core.TgNews.get_last_news()
    if last_news:

        bot.send_message(chat_id=chat_id, text=f'Вы уверены что хотите удалить новость:\n'
                                               f'"{last_news}"?',
                         reply_markup=keyboards.get_inline_confirm_delete_news_keyboard(last_news.id))
    else:
        bot.send_message(chat_id=chat_id, text='Список новостей пуст',
                         reply_markup=keyboards.get_news_keyboard())


@bot.callback_query_handler(func=lambda message: 'delete_news' in message.data)
def delete_last_news_confirm(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = json.loads(message.data)['delete_news']

    bot.delete_message(chat_id=chat_id, message_id=message_id)
    if data == 'cancel':
        return

    bot.send_message(chat_id=chat_id, text='Удаляем...')

    delete_news_id = data
    core.TgNews.delete_news(news_id=delete_news_id)

    bot.send_message(chat_id=chat_id, text='Новость удалена', reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def invalid_message(message):
    """
    Ответ на текст, который бот не понимает.

    Функция должна быть последней по порядку!
    :return:
    """
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_invalid_message_answer(chat_id=chat_id)
