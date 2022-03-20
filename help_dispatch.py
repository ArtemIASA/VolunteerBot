import logging
import states
import os
import google_sheets
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from dotenv import load_dotenv

load_dotenv()
OSA_TABLE = os.getenv('OSA_TABLE')
logger = logging.getLogger(__name__)


def send_again(update: Update):
    update.message.reply_text(
        'Дані було введено некоректно. '
        'Перевірте та Напишіть, будь ласка, ще раз '
        '🙏⤵️'
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
    )


def send_to_start(update: Update):
    reply_keyboard = [['✋ Потрібна допомога']]

    update.message.reply_text(
        'Обирайте потрібне ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )


def region(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['🛡 Речі для захисників'],
                      ['🍲 Обіди'],
                      ['💊 Ліки / засоби гігієни'],
                      ['🛒 Гуманітарна допомога (їжа, речі)'],
                      ['📖 Інше'],
                      ['❌ Відміна']
                      ]
    user = update.message.from_user
    text = update.message.text
    context.user_data['region'] = text
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Оберіть яка '
        'допомога потрібна ⤵️',
         reply_markup=ReplyKeyboardMarkup(
             reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.HELP_TYPE


def help_type(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['❌ Відміна']]
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    context.user_data['table_id'] = OSA_TABLE
    context.user_data['help_type'] = text
    logger.info("Text is: %s", text)
    if text == '📖 Інше':
        update.message.reply_text(
            'Опишіть докладно яка '
            'допомога потрібна ⤵️',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, resize_keyboard=True
            )
        )
    elif text == '🍲 Обіди':
        update.message.reply_text(
            'Напишіть кількість '
            'обідів ⤵️',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, resize_keyboard=True
            )
        )
    else:
        update.message.reply_text(
            'Напишіть назву '
            'та кількість ⤵️',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, resize_keyboard=True
            )
        )

    return states.HELP

def help(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    context.user_data['help'] = text
    logger.info("Text is: %s", text)
    update.message.reply_text(
        'Напишіть ваше імʼя '
        'та прізвище ⤵️',
    )

    return states.NAME

def name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if validate_name(text) is None:
        send_again(update)
        return states.NAME
    logger.info("Text is: %s", text)
    context.user_data['name'] = text
    update.message.reply_text(
        'Напишіть ваш номер '
        'телефону ⤵️'
    )

    return states.PHONE

def phone(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if validate_phone(text) is None:
        send_again(update)
        return states.PHONE
    logger.info("Text is: %s", text)
    context.user_data['phone'] = text
    update.message.reply_text(
        'Напишіть адресу, де потрібна допомога ⤵️',
    )

    return states.ADDRESS


def address(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if validate_address(text) is None:
        send_again(update)
        return states.ADDRESS
    logger.info("Text is: %s", text)
    context.user_data['address'] = text
    sheets = google_sheets.Sheets(context.user_data['help_type'], context.user_data['table_id'])
    sheets.add_all(context.user_data)
    update.message.reply_text(
        """Ми записали ваше звернення. Зачекайте на дзвінок, будь ласка. Постараємось допомогти вам якомога скоріше 🙏. Натисніть /start, якщо вам потрібно зробити ще один запит.""",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def validate_name(text:str):
    return re.fullmatch("^[А-Яа-яЁёЇїІіЄєʼ ,.'-]+$", text)

def validate_address(text:str):
    return re.fullmatch("^[А-Яа-я0-9ЁёЇїІіЄєʼ ,.'-/]+$", text)

def validate_phone(text:str):
    return re.fullmatch("^[0-9+]+$", text)