# coding: utf-8

import sqlite3

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
