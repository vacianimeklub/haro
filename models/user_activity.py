from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import engine, Base


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

Base.metadata.create_all(engine)
