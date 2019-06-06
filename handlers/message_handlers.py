# coding: utf-8

from models import session, Chat, User, UserActivity


def stats(bot, update):
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

    chat = Chat(
        update.message.chat_id,
        update.message.chat.title if update.message.chat.title else update.message.chat.type,
    )
    chat = session.merge(chat)
    session.add(chat)

    user_activity = UserActivity(
        user,
        chat,
        update.message.date
    )
    session.add(user_activity)
    session.commit()
