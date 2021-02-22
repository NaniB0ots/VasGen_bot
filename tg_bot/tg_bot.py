import telebot

from project.settings import TG_TOKEN

if not TG_TOKEN:
    raise ValueError('TG_TOKEN не может быть пустым')

bot = telebot.TeleBot(TG_TOKEN, threaded=False)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!')
