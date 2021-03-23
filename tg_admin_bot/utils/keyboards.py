from telebot import types
import json

MAX_CALLBACK_RANGE = 41


def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать трансляцию')
    btn2 = types.KeyboardButton('Новости')
    btn3 = types.KeyboardButton('Авторы')

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup


def get_inline_text_translation_matches_keyboard(matches_queryset):
    markup = types.InlineKeyboardMarkup()

    for match in matches_queryset:
        callback_data = json.dumps({'match': match.id})
        markup.add(types.InlineKeyboardButton(text=match.title, callback_data=callback_data))

    return markup


def get_stop_text_translation_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Стоп')

    markup.add(btn1)

    return markup


def get_news_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Опубликовать новость')
    btn2 = types.KeyboardButton('Удалить последнюю новость')
    btn3 = types.KeyboardButton('Основное меню')

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup


def get_cancel_write_news_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Отмена')

    markup.add(btn1)

    return markup
