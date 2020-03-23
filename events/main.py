# coding: utf-8

# events/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import metadata, start_mapper

# define engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
