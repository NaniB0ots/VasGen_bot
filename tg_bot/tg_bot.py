import json

from project.settings import TG_TOKEN
from tg_bot import core, models
from tg_bot.core import Bot
from tg_bot.utils import keyboards
import re

if not TG_TOKEN:
    raise ValueError('TG_TOKEN не может быть пустым')

bot = Bot(TG_TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    bot.send_message(chat_id=chat_id, text=bot.get_start_message(), reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(regexp='^Главное меню$')
def matches(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Главное меню', reply_markup=keyboards.get_main_menu_keyboard())


# Раздел "Матчи"

@bot.message_handler(regexp='^Матчи$')
def matches(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Матчи', reply_markup=keyboards.get_matches_keyboard())


@bot.message_handler(regexp='^Ближайший матч$')
def matches(message):
    chat_id = message.chat.id

    match = core.Match.get_nearest_match()

    if not match:
        bot.send_message(chat_id=chat_id, text='Ближайших матчей не предвидится')
        return

    try:
        match.users_for_text_translation.get(chat_id=chat_id)
        is_text_translation_active = True
    except models.TgUser.DoesNotExist:
        is_text_translation_active = False

    bot.send_message(chat_id=chat_id, text=core.Match.get_match_info(match),
                     reply_markup=keyboards.get_inline_match_keyboard(
                         match.id,
                         is_text_translation_active=is_text_translation_active))


@bot.message_handler(regexp='^Матчи в этом месяце$')
def matches(message):
    chat_id = message.chat.id
    message_id = message.message_id

    month, matches = core.Match.get_matches_this_month()
    bot.send_message(chat_id=chat_id, text=f'Список матчей\n'
                                           f'{month}')
    for match in matches:

        try:
            match.users_for_text_translation.get(chat_id=chat_id)
            is_text_translation_active = True
        except models.TgUser.DoesNotExist:
            is_text_translation_active = False

        bot.send_message(chat_id=chat_id, text=core.Match.get_match_info(match),
                         reply_markup=keyboards.get_inline_match_keyboard(
                             event_id=match.id,
                             is_text_translation_active=is_text_translation_active
                         ))


@bot.message_handler(regexp='^Турнирная таблица$')
def lore(message):
    chat_id = message.chat.id
    team_lore = '<Турнирная таблица>'
    bot.send_message(chat_id=chat_id, text=team_lore)


@bot.callback_query_handler(func=lambda message: 'enable_match_notif' in message.data)
def enable_match_notifications(message):
    """
    Включить напоминание о матче
    :param message:
    :return:
    """
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = json.loads(message.data)['enable_match_notif']

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=keyboards.get_inline_match_keyboard(event_id=data['id'],
                                                                                   is_notification_active=True,
                                                                                   is_text_translation_active=data[
                                                                                       'transl']))


@bot.callback_query_handler(func=lambda message: 'disable_match_notif' in message.data)
def disable_match_notifications(message):
    """
    Выключить напоминание о матче
    :param message:
    :return:
    """
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = json.loads(message.data)['disable_match_notif']

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=keyboards.get_inline_match_keyboard(event_id=data['id'],
                                                                                   is_notification_active=False,
                                                                                   is_text_translation_active=data[
                                                                                       'transl']
                                                                                   ))


@bot.callback_query_handler(func=lambda message: 'enable_translation' in message.data)
def enable_text_translation(message):
    """
    Включить текстовую трансляцию
    :param message:
    :return:
    """
    chat_id = message.message.chat.id
    message_id = message.message.message_id

    data = json.loads(message.data)['enable_translation']

    user = core.User(chat_id=chat_id)
    match = core.Match(match_id=data['id'])
    match.enable_text_translation(user=user)

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=keyboards.get_inline_match_keyboard(event_id=data['id'],
                                                                                   is_text_translation_active=True,
                                                                                   is_notification_active=data[
                                                                                       'notif']))


@bot.callback_query_handler(func=lambda message: 'disable_translation' in message.data)
def disable_text_translation(message):
    """
    Выключить текстовую трансляцию
    :param message:
    :return:
    """
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = json.loads(message.data)['disable_translation']

    user = core.User(chat_id=chat_id)
    match = core.Match(match_id=data['id'])
    match.disable_text_translation(user=user)

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                  reply_markup=keyboards.get_inline_match_keyboard(event_id=data['id'],
                                                                                   is_text_translation_active=False,
                                                                                   is_notification_active=data[
                                                                                       'notif']))


# Раздел "О команде"

@bot.message_handler(regexp='^О Команде$|^В раздел "О команде"$')
def about_team(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=f'О команде', reply_markup=keyboards.get_about_team_keyboard())


@bot.message_handler(regexp='^Тренерский состав$|^В раздел "Тренерский состав"$')
def get_trainers(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=f'Тренера', reply_markup=keyboards.get_coaches_keyboard())


@bot.message_handler(regexp='^Главный тренер$|^Второй тренер$')
def get_main_trainer(message):
    chat_id = message.chat.id
    post = message.text
    coach = core.Coaches.get_coach(post)
    main_coach_info = core.Coaches.get_coach_info(coach)
    bot.send_message(chat_id=chat_id, text=main_coach_info)


@bot.message_handler(regexp='^Игроки$|^В раздел "Игроки"$')
def get_players(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=f'Игроки', reply_markup=keyboards.get_players_keyboard())


@bot.message_handler(regexp='^Нападающие|^Защитники$|^Полузащитники$|^Вратари$')
def get_players(message):
    playing_positions = {'Нападающие': 'Нападающий', 'Защитники': 'Защитник', 'Полузащитники': 'Полузащитник',
                         'Вратари': 'Вратарь'}
    chat_id = message.chat.id
    playing_position = playing_positions[message.text]
    players = core.Players.get_players(playing_position)
    bot.send_message(chat_id=chat_id, text=f'{message.text}', reply_markup=keyboards.get_halfbacks_keyboard(players))


@bot.message_handler(regexp='^История команды$')
def lore(message):
    chat_id = message.chat.id
    team_lore = '<Краткая история команды>'
    bot.send_message(chat_id=chat_id, text=team_lore)


@bot.message_handler(regexp='^Мини-игры$')
def lore(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='<Мини-игры>')


@bot.message_handler(regexp=r'^Настройки')
def extra(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='<Настройки>')


@bot.message_handler(regexp=r'^Другое$')
def extra(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Другое', reply_markup=keyboards.extra_keyboard())


@bot.message_handler(regexp='^Авторы$')
def authors(message):
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id, text=bot.get_authors())


@bot.message_handler(regexp=r'(?:[А-ЯЁ][а-яё]+\s?){3}')
def players_info(message):
    pattern = re.compile(r'(?:[А-ЯЁ][а-яё]+\s?){3}')
    chat_id = message.chat.id
    full_name = message.text
    if re.fullmatch(pattern, full_name):
        player = core.Players.get_player(full_name)
        player_info = core.Players.get_player_info(player)
        bot.send_message(chat_id=chat_id, text=player_info)
    else:
        bot.send_invalid_message_answer(chat_id=chat_id)


@bot.message_handler(
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def invalid_message(message):
    """
    Ответ на текст, который бот не понимает.

    Функция должна быть последней по порядку!
    :return:
    """
    chat_id = message.chat.id

    bot.send_invalid_message_answer(chat_id=chat_id)
