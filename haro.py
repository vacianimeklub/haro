# coding: utf-8
from functools import wraps

import ipdb
import logging
import os
import sqlite3

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))
LIST_OF_ADMINS = [ADMIN_USER_ID]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            bot.send_message(chat_id=update.message.chat_id, text="Nyem, haro. {} user id nyem jó.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(BOT_TOKEN)
dispatcher = updater.dispatcher
db_conn = sqlite3.connect('haro.sqlite')
cursor = db_conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER, 
        username TEXT,
        chat_id INTEGER,
        chat_title TEXT, 
        datetime TEXT
    )
''')
db_conn.commit()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Haro elindult! Haro elindult!")

def echo(bot, update):
    if "Haro" in update.message.text and "?" in update.message.text:
        update.message.reply_text('Haro figyel! Haro figyel!')

    db_conn = sqlite3.connect('haro.sqlite')
    c = db_conn.cursor()
    c.execute('''
            INSERT INTO user_activity (id, username, chat_id, chat_title, datetime) VALUES (?, ?, ?, ?, ?)
        ''', (
            update.message.from_user.id,
            update.message.from_user.username,
            update.message.chat_id,
            update.message.chat.title if update.message.chat.title else update.message.chat.type,
            str(update.message.date)
        ))
    db_conn.commit()

@restricted
def dump(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Adatok küldése, adatok küldése!")
    bot.send_document(chat_id=update.message.chat_id, document=open('haro.sqlite', 'rb'))

start_handler = CommandHandler('start', start)
dump_handler = CommandHandler('dump', dump)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(dump_handler)
dispatcher.add_handler(echo_handler)


updater.start_polling()
updater.idle()
db_conn.close()
