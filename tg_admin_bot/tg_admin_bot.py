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
    data = json.loads(message.data)['match']

    match = core.TextTranslation.get_match_query(match_id=data)
    if match:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=match.title)
        bot.send_message(chat_id=chat_id,
                         text='Окей! Запускаем вещание...\n'
                              'Все, Вы в эфире.\n\n'
                              'Для того, чтобы прекратить трансляцию, необходимо нажать на кнопку “Стоп”',
                         reply_markup=keyboards.get_stop_text_translation_keyboard())
    else:
        bot.send_message(chat_id=chat_id,
                         text='Что-то пошло не так... Попробуйте ещё раз',
                         reply_markup=keyboards.get_main_menu_keyboard())


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


@bot.message_handler(regexp='^Опубликовать новость$')
def news(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.is_authenticated():
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Для того, чтобы опубликовать новость, '
                                           'напишите текст новости с клавиатуры и нажмите “Опубликовать”.\n\n'
                                           'Ждем вестей!')
