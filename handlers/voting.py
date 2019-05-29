# coding: utf-8

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    RegexHandler,
    ConversationHandler,
)

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

STATE__GET_TITLE, STATE__GET_DESCRIPTION, STATE__GET_ANSWERS, STATE__GET_SELECTION_MODE = range(4)
SINGLE_CHOICE = u'Egy legyen választható'
MULTIPLE_CHOICE = u'Lehessen többet is kiválasztani'


def get_setup_voting_conversation_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler('szavazas', vote_setup_start),
        ],

        states={
            STATE__GET_TITLE: [
                MessageHandler(Filters.text, vote_setup_process_title_response),
            ],

            STATE__GET_DESCRIPTION: [
                MessageHandler(Filters.text, vote_setup_process_description_response),
                # CommandHandler('skip', skip_description),
            ],

            STATE__GET_ANSWERS: [
                MessageHandler(Filters.text, vote_setup_process_answers),
            ],

            STATE__GET_SELECTION_MODE: [
                RegexHandler(
                    u'^({single}|{multiple})$'.format(
                        single=SINGLE_CHOICE,
                        multiple=MULTIPLE_CHOICE
                    ),
                    vote_setup_process_mode_selection,
                ),
            ],
        },

        fallbacks=[
            CommandHandler('megsem', cancel_setup_voting),
        ]
    )


def vote_setup_start(bot, update):
    logger.info(u'voting starts')
    update.message.reply_text(u'Csináljunk egy szavazást! Mi legyen a címe?')

    return STATE__GET_TITLE


def vote_setup_process_title_response(bot, update):
    logger.info(u'got title response: {}'.format(update.message.text))
    update.message.reply_text(u'Okés. Mi legyen a leírása?')

    return STATE__GET_DESCRIPTION


def vote_setup_process_description_response(bot, update):
    logger.info(u'got description response: {}'.format(update.message.text))
    update.message.reply_text(
        u'Milyen válaszok legyenek? '
        u'(Írd le egymás után az összeset, két darab | karakterrel elválasztva.)'
    )

    return STATE__GET_ANSWERS


def vote_setup_process_answers(bot, update):
    logger.info(u'got answers response: {}'.format(update.message.text))

    if '||' not in update.message.text:
        logger.info(u'improper answers response, retrying')
        update.message.reply_text(
            u'Nem adtál meg elég választ! Próbáljuk újra. '
            u'(Írd le egymás után az összeset, két darab | karakterrel elválasztva.)'
        )
        return STATE__GET_ANSWERS

    reply_keyboard = [[SINGLE_CHOICE, MULTIPLE_CHOICE]]
    update.message.reply_text(
        u'Most már csak azt kell eldöntened, lehessen-e több választ megadni egyszerre.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return STATE__GET_SELECTION_MODE


def vote_setup_process_mode_selection(bot, update):
    logger.info(u'got mode selection response: {}'.format(update.message.text))
    update.message.reply_text(u'Készen is vagyunk, köszi!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel_setup_voting(bot, update):
    logger.info(u'user cancelled')
    update.message.reply_text(u'Akkor semmi :)')

    return ConversationHandler.END
