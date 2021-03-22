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
                              message_id: int,
                              is_notification_active=False,
                              is_text_translation_active=False):
    markup = types.InlineKeyboardMarkup()
    if not is_notification_active:
        notification_text = 'Подписаться на уведомление'
    else:
        notification_text = 'Отписаться от уведомления'
    markup.add(types.InlineKeyboardButton(text=notification_text, callback_data='qwe'), )

    if not is_text_translation_active:
        translation_text = 'Подписаться на текстовую трансляцию'
    else:
        translation_text = 'Отписаться от текстовой трансляции'

    markup.add(types.InlineKeyboardButton(text=translation_text, callback_data='123'))
    return markup
