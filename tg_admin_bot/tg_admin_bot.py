import telebot

from project.settings import TG_TOKEN_ADMIN

if not TG_TOKEN_ADMIN:
    raise ValueError('TG_TOKEN_ADMIN не может быть пустым')

bot = telebot.TeleBot(TG_TOKEN_ADMIN, threaded=False)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!')
