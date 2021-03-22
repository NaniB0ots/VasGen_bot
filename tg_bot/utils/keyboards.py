from telebot import types

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
