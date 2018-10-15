from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import engine, Base, users


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer)
    chat_title = Column(String)
    datetime = Column(DateTime)

    user = relationship("User", back_populates="activity")

    def __init__(self, user, chat_id, chat_title, datetime):
        self.user = user
        self.chat_id = chat_id
        self.chat_title = chat_title
        self.datetime = datetime

Base.metadata.create_all(engine)