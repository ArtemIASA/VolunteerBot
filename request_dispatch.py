import logging
import states
from help_dispatch import send_to_start
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logger = logging.getLogger(__name__)

def request(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Деснянський'], ['Святошинський'],
                       ['Дніпровський'], ['Печерський'],
                       ['Голосіївський'], ['Дарницький'],
                       ['Соломянський'], ['Оболонський'],
                       ['Шевченківський'], ['Подільський']
                       ]

    user = update.message.from_user
    text = update.message.text
    logger.info("Gender of %s: %s", user.first_name, text)
    if text == '/start':
        send_to_start(update)
        return states.REQUEST
    update.message.reply_text(
        'Оберіть район, де '
        'потрібна допомога ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.REGION