from sqlalchemy import Column, DateTime, Integer, String

from models import engine, Base

class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    chat_id = Column(Integer)
    chat_title = Column(String)
    datetime = Column(DateTime)

    def __init__(self, user_id, username, chat_id, chat_title, datetime):
        self.user_id = user_id
        self.username = username
        self.chat_id = chat_id
        self.chat_title = chat_title
        self.datetime = datetime

Base.metadata.create_all(engine)