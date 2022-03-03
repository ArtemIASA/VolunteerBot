import logging
import states
import google_sheets
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
sheets = google_sheets.Sheets("Sheet1")
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
    """Stores the selected gender and asks for a photo."""
    # reply_keyboard = [['Мені потрібні автоволонтери'],
    #                   ['Мені потрібні речі для захисників'],
    #                   ['Мені потрібні ліки / засоби гігієни'],
    #                   ['Мені потрібна допомога волонтерів руками'],
    #                   ['Мені потрібна гуманітарна допомога (їжа, речі)'],
    #                   ['Мого запиту немає в списку']
    #                   ]
    reply_keyboard = [['❌ Відміна']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишіть яка '
        'допомога потрібна ⤵️',
         reply_markup=ReplyKeyboardMarkup(
             reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.HELP


def help(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['❌ Відміна']]
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    sheets.add_help_info(text)
    logger.info("Text is: %s", text)
    update.message.reply_text(
        'Напишіть ваше імʼя '
        'та прізвище ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.NAME


def name(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['❌ Відміна']]
    print(context.chat_data)
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if sheets.validate_name(text) is None:
        send_again(update)
        return states.NAME
    logger.info("Text is: %s", text)
    sheets.add_name(update.message.text)
    update.message.reply_text(
        'Напишіть ваш номер '
        'телефону ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.PHONE

def phone(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['❌ Відміна']]
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if sheets.validate_phone(text) is None:
        send_again(update)
        return states.PHONE
    logger.info("Text is: %s", text)
    sheets.add_phone(update.message.text)
    update.message.reply_text(
        'Напишіть адресу, де потрібна допомога ⤵️',

        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.ADDRESS


def address(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    text = update.message.text
    if text == '❌ Відміна':
        send_to_start(update)
        return states.REQUEST
    if sheets.validate_address(text) is None:
        send_again(update)
        return states.ADDRESS
    logger.info("Text is: %s", text)
    sheets.add_address(update.message.text)
    update.message.reply_text(
        """Ми записали ваше звернення.
    Зачекайте на дзвінок, будь ласка.
    Постараємось допомогти вам якомога скоріше 🙏""",

        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )

    )
    return ConversationHandler.END