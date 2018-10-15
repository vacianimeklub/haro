# coding: utf-8

from models import session
from models.user_activity import UserActivity
from models.users import User

def echo(bot, update):
    if "Haro" in update.message.text and "?" in update.message.text:
        update.message.reply_text('Haro figyel! Haro figyel!')

    user = User(
        update.message.from_user.id, 
        update.message.from_user.first_name, 
        update.message.from_user.last_name, 
        update.message.from_user.username
    )
    user = session.merge(user)
    session.add(user)

    user_activity = UserActivity(
        user,
        update.message.chat_id,
        update.message.chat.title if update.message.chat.title else update.message.chat.type,
        update.message.date
    )
    session.add(user_activity)
    session.commit()
