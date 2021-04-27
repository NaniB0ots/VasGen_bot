from telebot import types
import json

MAX_CALLBACK_RANGE = 41


def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Матчи')
    btn2 = types.KeyboardButton('О Команде')
    btn3 = types.KeyboardButton('Мини-игры')
    btn4 = types.KeyboardButton('Настройки')
    btn5 = types.KeyboardButton('Другое')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    return markup


def get_matches_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Ближайший матч')
    btn2 = types.KeyboardButton('Матчи в этом месяце')
    btn3 = types.KeyboardButton('Турнирная таблица')
    btn4 = types.KeyboardButton('Главное меню')

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


def get_inline_match_keyboard(event_id: int,
                              is_notification_active=False,
                              is_text_translation_active=False):
    markup = types.InlineKeyboardMarkup()
    if not is_notification_active:
        notification_text = 'Подписаться на уведомление'
        notification_callback_data = json.dumps({
            'enable_match_notif':
                {
                    'id': event_id,
                    'transl': is_text_translation_active
                }
        })
    else:
        notification_text = 'Отписаться от уведомления ✅'
        notification_callback_data = json.dumps({
            'disable_match_notif':
                {
                    'id': event_id,
                    'transl': is_text_translation_active
                }
        })

    markup.add(types.InlineKeyboardButton(text=notification_text, callback_data=notification_callback_data))

    if not is_text_translation_active:
        translation_text = 'Подписаться на текстовую трансляцию '
        translation_callback_data = json.dumps({
            'enable_translation':
                {
                    'id': event_id,
                    'notif': is_notification_active
                }
        })
    else:
        translation_text = 'Отписаться от текстовой трансляции ✅'
        translation_callback_data = json.dumps({
            'disable_translation':
                {
                    'id': event_id,
                    'notif': is_notification_active
                }
        })

    markup.add(types.InlineKeyboardButton(text=translation_text, callback_data=translation_callback_data))
    return markup


def get_about_team_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Тренерский состав')
    btn2 = types.KeyboardButton('Игроки')
    btn3 = types.KeyboardButton('История команды')
    btn4 = types.KeyboardButton('Главное меню')

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


def get_coaches_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Главный тренер')
    btn2 = types.KeyboardButton('Второй тренер')
    btn3 = types.KeyboardButton('В раздел "О команде"')
    btn4 = types.KeyboardButton('Главное меню')

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup


def get_main_coach_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('В раздел "Тренерский состав"')
    btn2 = types.KeyboardButton('Главное меню')

    markup.add(btn1, btn2)
    return markup


def get_players_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Нападающие')
    btn2 = types.KeyboardButton('Защитники')
    btn3 = types.KeyboardButton('Полузащитники')
    btn4 = types.KeyboardButton('Вратари')
    btn5 = types.KeyboardButton('В раздел "О команде"')
    btn6 = types.KeyboardButton('Главное меню')

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    return markup


def extra_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Авторы')
    btn2 = types.KeyboardButton('Главное меню')

    markup.add(btn1)
    markup.add(btn2)
    return markup


def get_halfbacks_keyboard(players):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for player in players:
        lastname = player.lastname
        firstname = player.firstname
        patronymic = player.patronymic
        btn = types.KeyboardButton(f'{lastname} {firstname} {patronymic}')
        markup.add(btn)

    btn1 = types.KeyboardButton(f'В раздел "Игроки"')
    btn2 = types.KeyboardButton(f'Главное меню')
    markup.add(btn1, btn2)
    return markup

