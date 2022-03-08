import logging
import os
import states
from request_dispatch import request
from help_dispatch import *
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

load_dotenv()
token = os.getenv("TOKEN")
port = os.getenv("PORT")
webhook_host = os.getenv("HOST_IP")
webapp_url = f"https://{webhook_host}:{port}/"
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['✋ Потрібна допомога']]

    update.message.reply_text(
        'Обирайте потрібне ⤵️',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )

    return states.REQUEST


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            states.REQUEST: [MessageHandler(Filters.regex('^(✋ Потрібна допомога)$'), request)],
            states.REGION: [MessageHandler(Filters.regex('^(Деснянський|Святошинський|Дніпровський|Печерський|Голосіївський|Дарницький|Соломянський|Оболонський|Шевченківський|Подільський)$'), region)],
            states.HELP_TYPE: [MessageHandler(Filters.regex('^(🍲|🛡|💊|🛒|📖|❌)'), help_type)],
            states.HELP: [MessageHandler(Filters.text, help)],
            states.NAME: [MessageHandler(Filters.text, name)],
            states.PHONE: [MessageHandler(Filters.text, phone)],
            states.ADDRESS: [MessageHandler(Filters.text, address)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    # updater.start_webhook('0.0.0.0', port=port, url_path=token, key='url_private.key',
    #                   cert='url_cert.pem', webhook_url=webapp_url + token)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()