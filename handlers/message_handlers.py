# coding: utf-8

from models import session
from models.user_activity import UserActivity

def echo(bot, update):
    if "Haro" in update.message.text and "?" in update.message.text:
        update.message.reply_text('Haro figyel! Haro figyel!')

    user_activity = UserActivity(
        update.message.from_user.id,
        update.message.from_user.username,
        update.message.chat_id,
        update.message.chat.title if update.message.chat.title else update.message.chat.type,
        update.message.date
    )
    session.add(user_activity)
    session.commit()
