# coding: utf-8

import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from handlers.command_handlers import start, dump
from handlers.message_handlers import echo
from settings import BOT_TOKEN


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def setup_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dump_handler = CommandHandler('dump', dump)
    echo_handler = MessageHandler(Filters.text, echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dump_handler)
    dispatcher.add_handler(echo_handler)


if __name__ == '__main__':
    setup_logging()

    updater = Updater(BOT_TOKEN)
    setup_handlers(updater.dispatcher)
    updater.start_polling()
    updater.idle()
    