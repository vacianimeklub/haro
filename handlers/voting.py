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

from models import session, User, Voting, VotingOption

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

STATE__GET_TITLE, STATE__GET_DESCRIPTION, STATE__GET_ANSWERS, STATE__GET_SELECTION_MODE = range(4)
SINGLE_CHOICE = u'Egy legyen választható'
MULTIPLE_CHOICE = u'Lehessen többet is kiválasztani'


def get_setup_voting_conversation_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler('szavazas', vote_setup_start, pass_chat_data=True),
        ],

        states={
            STATE__GET_TITLE: [
                MessageHandler(
                    Filters.text,
                    vote_setup_process_title_response,
                    pass_chat_data=True
                ),
            ],

            STATE__GET_DESCRIPTION: [
                MessageHandler(
                    Filters.text,
                    vote_setup_process_description_response,
                    pass_chat_data=True
                ),
                # CommandHandler('skip', skip_description),
            ],

            STATE__GET_ANSWERS: [
                MessageHandler(
                    Filters.text,
                    vote_setup_process_answers,
                    pass_chat_data=True
                ),
            ],

            STATE__GET_SELECTION_MODE: [
                RegexHandler(
                    u'^({single}|{multiple})$'.format(
                        single=SINGLE_CHOICE,
                        multiple=MULTIPLE_CHOICE
                    ),
                    vote_setup_process_mode_selection,
                    pass_chat_data=True
                ),
            ],
        },

        fallbacks=[
            CommandHandler('megsem', cancel_setup_voting, pass_chat_data=True),
        ]
    )


def vote_setup_start(bot, update, chat_data):
    chat_data['voting'] = {}
    logger.info(u'voting starts')
    update.message.reply_text(u'Csináljunk egy szavazást! Mi legyen a címe?')

    return STATE__GET_TITLE


def vote_setup_process_title_response(bot, update, chat_data):
    chat_data['voting']['title'] = update.message.text
    logger.info(u'got title response: {}'.format(update.message.text))
    update.message.reply_text(u'Okés. Mi legyen a leírása?')

    return STATE__GET_DESCRIPTION


def vote_setup_process_description_response(bot, update, chat_data):
    chat_data['voting']['description'] = update.message.text
    logger.info(u'got description response: {}'.format(update.message.text))
    update.message.reply_text(
        u'Milyen válaszok legyenek? '
        u'(Írd le egymás után az összeset, két darab | karakterrel elválasztva.)'
    )

    return STATE__GET_ANSWERS


def vote_setup_process_answers(bot, update, chat_data):
    logger.info(u'got answers response: {}'.format(update.message.text))

    if '||' not in update.message.text:
        logger.info(u'improper answers response, retrying')
        update.message.reply_text(
            u'Nem adtál meg elég választ! Próbáljuk újra. '
            u'(Írd le egymás után az összeset, két darab | karakterrel elválasztva.)'
        )
        return STATE__GET_ANSWERS

    chat_data['voting']['answers'] = update.message.text.split('||')

    reply_keyboard = [[SINGLE_CHOICE, MULTIPLE_CHOICE]]
    update.message.reply_text(
        u'Most már csak azt kell eldöntened, lehessen-e több választ megadni egyszerre.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return STATE__GET_SELECTION_MODE


def vote_setup_process_mode_selection(bot, update, chat_data):
    logger.info(u'got mode selection response: {}'.format(update.message.text))

    chat_data['voting']['multi'] = update.message.text == MULTIPLE_CHOICE

    update.message.reply_text(u'Készen is vagyunk, köszi!', reply_markup=ReplyKeyboardRemove())

    save_voting(update.message.from_user, chat_data['voting'])

    return ConversationHandler.END


def cancel_setup_voting(bot, update, chat_data):
    logger.info(u'user cancelled')
    update.message.reply_text(u'Akkor semmi :)')

    return ConversationHandler.END


def save_voting(from_user, voting_data):
    creator_user = User(
        from_user.id,
        from_user.first_name,
        from_user.last_name,
        from_user.username
    )
    creator_user = session.merge(creator_user)
    session.add(creator_user)

    options = []
    for voting_option in voting_data['answers']:
        option = VotingOption(voting_option)
        option = session.merge(option)
        session.add(option)
        options.append(option)

    voting = Voting(
        creator=creator_user,
        title=voting_data['title'],
        description=voting_data['description'],
        is_multi_choice=voting_data['multi'],
        options=options,
    )
    voting = session.merge(voting)
    session.add(voting)
    session.commit()
