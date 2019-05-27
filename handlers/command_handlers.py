# coding: utf-8

from sqlalchemy.sql import func
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .const import ACTIVE_ENTRY_TEXT_SUFFIX, DUMMY_VOTE_ENTRIES
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

def get_vote_entries(active_keys=[]):
    entries = DUMMY_VOTE_ENTRIES.copy()
    for key in active_keys:
        if key in entries.keys():
            entries[key] = toggle_vote_entry_text(entries[key])
    return entries

def get_voting_reply_markup(vote_entries):
    if not vote_entries:
        return None

    button_list = [InlineKeyboardButton(entry, callback_data=id) for id, entry in vote_entries.items()]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

def toggle_vote_entry_text(entry_text):
    if entry_text.endswith(ACTIVE_ENTRY_TEXT_SUFFIX):
        return entry_text.replace(ACTIVE_ENTRY_TEXT_SUFFIX, '')
    return "{text}{suffix}".format(text=entry_text, suffix=ACTIVE_ENTRY_TEXT_SUFFIX)

@admin_only
def vote(bot, update):
    reply_markup = get_voting_reply_markup(get_vote_entries())
    bot.send_message(chat_id=update.message.chat_id, text="Szavazzunk! Szavazzunk!", reply_markup=reply_markup)
    # switch_inline_query is going to be necessary for the last message which will publish the vote

def vote_callback(bot, update):
    bot.answer_callback_query(update.callback_query.id, text='Vettem! Vettem!')
    # below, we will need to merge the state with the earlier one if we want to keep earlier responses, or 
    # ignore the earlier state (as we do now):
    reply_markup = get_voting_reply_markup(get_vote_entries([update.callback_query.data]))
    origin_message_from_bot = update.callback_query.message
    bot.edit_message_text(
        text=u"Azt választottad, hogy '{}'!".format(update.callback_query.data),
        chat_id=origin_message_from_bot.chat_id,
        message_id=origin_message_from_bot.message_id,
        reply_markup=reply_markup
    )


def last_message(bot, update):
    q = session.query(UserActivity).join("user").join("chat").group_by(User.id)
