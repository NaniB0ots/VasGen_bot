from project.settings import TG_TOKEN
from tg_bot import core
from tg_bot.core import Bot
from tg_bot.utils import keyboards

if not TG_TOKEN:
    raise ValueError('TG_TOKEN не может быть пустым')

bot = Bot(TG_TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=bot.get_start_message(), reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(regexp='^Главное меню$')
def matches(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Главное меню', reply_markup=keyboards.get_main_menu_keyboard())


@bot.message_handler(regexp='^Матчи$')
def matches(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Матчи', reply_markup=keyboards.get_matches_keyboard())


@bot.message_handler(regexp='^Матчи в этом месяце$')
def matches(message):
    chat_id = message.chat.id
    month, matches = core.Match.get_matches_this_month()
    bot.send_message(chat_id=chat_id, text=f'Список матчей\n'
                                           f'{month}')
    for match in matches:
        bot.send_message(chat_id=chat_id, text=f'{match.title}\n'
                                               f'{match.date_of_the_event.date().strftime("%d.%m.%Y")}\n\n'
                                               f'{match.description}',
                         reply_markup=keyboards.get_inline_match_keyboard(event_id=match.id,
                                                                          message_id=message.chat.id))
