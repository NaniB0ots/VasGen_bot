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


def authorization(message):
    chat_id = message.chat.id
    token = message.text
    username = message.from_user.username
    if core.User.authorization(chat_id=chat_id, token=token, username=username):
        bot.send_message(chat_id=chat_id, text=bot.get_instruction(), reply_markup=keyboards.get_main_menu_keyboard())
    else:
        msg = bot.send_message(chat_id=chat_id, text=bot.get_register_message())
        bot.register_next_step_handler(msg, authorization)
