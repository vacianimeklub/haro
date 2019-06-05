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

    options = relationship('VotingOptions', back_populates='voting')
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


class VotingOptions(Base):
    __tablename__ = "voting_options"

    id = Column(Integer, primary_key=True)
    voting_id = Column(Integer, ForeignKey('voting.id'))
    option = Column(String)

    voting = relationship('Voting', back_populates='options')

    def __init__(self, option):
        self.option = option
