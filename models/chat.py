from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    chat_title = Column(String)

    activity = relationship("UserActivity", back_populates="chat")

    def __init__(self, id, chat_title):
        self.id = id
        self.chat_title = chat_title
