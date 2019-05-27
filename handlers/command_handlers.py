# coding: utf-8

from sqlalchemy.sql import func
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .helpers import admin_only, build_menu

from models import session
from models.user_activity import UserActivity
from models.user import User
from models.chat import Chat
from settings import SQLITE_PATH

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Haro elindult! Haro elindult!")


@admin_only
def dump(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Adatok küldése, adatok küldése!")
    bot.send_document(chat_id=update.message.chat_id, document=open(SQLITE_PATH, 'rb'))


@admin_only
def vote(bot, update):
    button_list = [
        InlineKeyboardButton("Alma", callback_data=u'alma'),
        InlineKeyboardButton("Körte", callback_data=u'körte'),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text="Szavazzunk! Szavazzunk!", reply_markup=reply_markup)
    # switch_inline_query is going to be necessary for the last message which will publish the vote

def vote_callback(bot, update):
    bot.answer_callback_query(update.callback_query.id, text='Vettem! Vettem!')
    button_list = [
        InlineKeyboardButton("Alma ✅" if update.callback_query.data == u'alma' else "Alma", callback_data=u'alma'),
        InlineKeyboardButton("Körte ✅" if update.callback_query.data == u'körte' else "Körte", callback_data=u'körte'),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    origin_message_from_bot = update.callback_query.message
    bot.edit_message_text(
        text=u"Azt választottad, hogy '{}'!".format(update.callback_query.data),
        chat_id=origin_message_from_bot.chat_id,
        message_id=origin_message_from_bot.message_id,
        reply_markup=reply_markup
    )


def last_message(bot, update):
    q = session.query(UserActivity).join("user").join("chat").group_by(User.id)
