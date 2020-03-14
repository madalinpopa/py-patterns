# coding: utf-8

# repository/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# define engine
engine = create_engine("sqlite:///repo.db", echo=True)

