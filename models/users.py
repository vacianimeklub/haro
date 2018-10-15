from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import engine, Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

    activity = relationship("UserActivity", back_populates="user")
    
    def __init__(self, id, first_name, last_name, username):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

Base.metadata.create_all(engine)