# coding: utf-8

from .helpers import admin_only
from models import session, User, UserActivity
from settings import SQLITE_PATH


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Haro elindult! Haro elindult!")


@admin_only
def dump(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Adatok küldése, adatok küldése!")
    bot.send_document(chat_id=update.message.chat_id, document=open(SQLITE_PATH, 'rb'))


def last_message(bot, update):
    session.query(UserActivity).join("user").join("chat").group_by(User.id)
