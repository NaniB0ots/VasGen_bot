from telebot import types
import json

MAX_CALLBACK_RANGE = 41


def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать трансляцию')
    btn2 = types.KeyboardButton('Опубликовать новость')
    btn3 = types.KeyboardButton('Авторы')

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup
