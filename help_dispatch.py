import logging
import states
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

def region(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Мені потрібні автоволонтери'],
                      ['Мені потрібні речі для захисників'],
                      ['Мені потрібні ліки / засоби гігієни'],
                      ['Мені потрібна допомога волонтерів руками'],
                      ['Мені потрібна гуманітарна допомога (їжа, речі)'],
                      ['Мого запиту немає в списку']
                      ]

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишіть яка '
        'допомога потрібна ⤵️',
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
    )

    return states.NAME

def help(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Мені потрібні автоволонтери'],
                      ['Мені потрібні речі для захисників'],
                      ['Мені потрібні ліки / засоби гігієни'],
                      ['Мені потрібна допомога волонтерів руками'],
                      ['Мені потрібна гуманітарна допомога (їжа, речі)'],
                      ['Мого запиту немає в списку']
                      ]

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишіть ваше імʼя '
        'та прізвище ⤵️'
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
        )

    return states.PHONE

def name(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Мені потрібні автоволонтери'],
                      ['Мені потрібні речі для захисників'],
                      ['Мені потрібні ліки / засоби гігієни'],
                      ['Мені потрібна допомога волонтерів руками'],
                      ['Мені потрібна гуманітарна допомога (їжа, речі)'],
                      ['Мого запиту немає в списку']
                      ]

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишіть ваш номер '
        'телефону ⤵️',
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
    )

    return states.PHONE

def phone(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Мені потрібні автоволонтери'],
                      ['Мені потрібні речі для захисників'],
                      ['Мені потрібні ліки / засоби гігієни'],
                      ['Мені потрібна допомога волонтерів руками'],
                      ['Мені потрібна гуманітарна допомога (їжа, речі)'],
                      ['Мого запиту немає в списку']
                      ]

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишіть адресу, де потрібна допомога'

        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
    )

    return states.ADDRESS


def address(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    reply_keyboard = [['Мені потрібні автоволонтери'],
                      ['Мені потрібні речі для захисників'],
                      ['Мені потрібні ліки / засоби гігієни'],
                      ['Мені потрібна допомога волонтерів руками'],
                      ['Мені потрібна гуманітарна допомога (їжа, речі)'],
                      ['Мого запиту немає в списку']
                      ]

    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        """Ми записали ваше звернення.
        Почекайте на дзвінок, будь ласка.
        Постараємось допомогти вам якомога скоріше""",

        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        # )
    )