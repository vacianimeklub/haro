from datetime import datetime
from sqlalchemy import (
    create_engine,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from settings import SQLALCHEMY_SQLITE_PATH


engine = create_engine(SQLALCHEMY_SQLITE_PATH, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

    activity = relationship("UserActivity", back_populates="user")
    created_votings = relationship('Voting', back_populates='creator')
    votes = relationship('Vote', back_populates='voter')

    def __init__(self, id, first_name, last_name, username):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    chat_title = Column(String)

    activity = relationship("UserActivity", back_populates="chat")

    def __init__(self, id, chat_title):
        self.id = id
        self.chat_title = chat_title


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.id'))
    datetime = Column(DateTime)

    user = relationship("User", back_populates="activity")
    chat = relationship("Chat", back_populates="activity")

    def __init__(self, user, chat, datetime):
        self.user = user
        self.chat = chat
        self.datetime = datetime


class Voting(Base):
    __tablename__ = "voting"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_multi_choice = Column(Boolean)
    creator_user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

    options = relationship('VotingOption', back_populates='voting')
    creator = relationship(
        'User',
        back_populates='created_votings',
        foreign_keys='Voting.creator_user_id',
    )

    def __init__(self, creator, title, description, is_multi_choice, options):
        self.creator = creator
        self.title = title
        self.description = description
        self.is_multi_choice = is_multi_choice
        self.options = options

        self.created_at = datetime.now()


class VotingOption(Base):
    __tablename__ = "voting_options"

    id = Column(Integer, primary_key=True)
    voting_id = Column(Integer, ForeignKey('voting.id'))
    option = Column(String)

    voting = relationship('Voting', back_populates='options')
    votes = relationship('Vote', back_populates='voting_option')

    def __init__(self, option):
        self.option = option


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    voting_option_id = Column(Integer, ForeignKey('voting_options.id'))

    voting_option = relationship('VotingOption', back_populates='votes')
    voter = relationship('User', back_populates='votes')

    def __init__(self, voter, voting_option):
        self.voter = voter
        self.voting_option = voting_option
