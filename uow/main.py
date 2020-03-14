# coding: utf-8

# uow/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Line, Order
from orm import metadata, start_mapper

from repo import SqlRepository


# define engine
engine = create_engine("sqlite:///repo.db")

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables
    metadata.create_all(bind=engine)

    # initiate repository
    repo = SqlRepository(session)


if __name__ == "__main__":
    main()
