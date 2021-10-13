import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from core.constants import TELEGRAM_TOKEN
from db.tasks import get_upcoming_tasks

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_tasks(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Retrieving tasks...')
    tasks = await get_upcoming_tasks()
    update.message.reply_text(str(tasks[1].values()))


def unknown_request(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Sorry, I do not recognise that request.')


def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Handle the '/tasks' command
    dispatcher.add_handler(CommandHandler('tasks', get_tasks))

    # Handle unrecognised commands or responses
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_request))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
