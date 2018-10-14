# coding: utf-8

from .helpers import restricted

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Haro elindult! Haro elindult!")


@restricted
def dump(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Adatok küldése, adatok küldése!")
    bot.send_document(chat_id=update.message.chat_id, document=open('haro.sqlite', 'rb'))
