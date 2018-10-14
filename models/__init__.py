from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import SQLITE_PATH, SQLALCHEMY_SQLITE_PATH


engine = create_engine(SQLALCHEMY_SQLITE_PATH, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
