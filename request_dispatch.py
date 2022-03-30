import logging
import states
from bank_accounts import *
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
                       ['Шевченківський'], ['Подільський'],
                       ['❌ Відміна']
                       ]
    reply_keyboard_sup = [['🏦 Реквізити для фінансової підтримки / 🏦 Bank details'],
                      ['❌ Відміна / ❌ Cancel'],
                      ]
    user = update.message.from_user
    text = update.message.text
    logger.info("Gender of %s: %s", user.first_name, text)
    if text == '/start' or '↩️' in text:
        send_to_start(update)
        return states.REQUEST
    if '💪' in text:
        update.message.reply_text(
            'Оберіть як ви хочете допомогти ⤵️ / Select how you want to help ⤵️',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_sup, one_time_keyboard=True, resize_keyboard=True
            )
        )
        return states.DONATION
    update.message.reply_text(
        'Оберіть район, де '
        'потрібна допомога ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.REGION


def donate(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['💳 Реквізити для фінансової підтримки в гривні ₴ / bank details for donations in UAH 💸'],
                      ['💳 Реквізити для фінансової підтримки в євро € / bank details for donations in EUR 💶'],
                      ['💳 Реквізити для фінансової підтримки в доларі / bank details for donations in USD 💵'],
                      ['❌ Відміна / ❌ Cancel'],
                      ]
    text = update.message.text
    if text == '❌ Відміна' or text == '/start':
        send_to_start(update)
        return states.REQUEST
    update.message.reply_text(
        'Обирайте потрібне ⤵️ / Select ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )
    return states.ACCOUNT


def bank_account(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [
                      ['↩️ Назад / ↩️ Return'],
                      ]
    text = update.message.text
    if text == '❌ Відміна' or text == '/start':
        send_to_start(update)
        return states.REQUEST
    if 'UAH' in text:
        update.message.reply_text(
            uah_bank,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    elif 'USD' in text:
        update.message.reply_text(
            usd_bank,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    elif 'EUR' in text:
        update.message.reply_text(
            eur_bank,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    return states.REQUEST

