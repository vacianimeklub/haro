# coding: utf-8

from functools import wraps

from settings import LIST_OF_ADMINS

def admin_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            bot.send_message(chat_id=update.message.chat_id, text="Nyem, haro. {} user id nyem jó.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
