from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from models import Base


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
