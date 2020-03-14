# coding: utf-8

# repository/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repository.orm import metadata, start_mapper
from repository.model import User, Profile

# define engine
engine = create_engine("sqlite:///repo.db", echo=True)

# create all tables
metadata.create_all(bind=engine)

# create session
session = sessionmaker(bind=engine)()


def main():
    start_mapper()
    user = User("ed", "secret")
    profile = Profile("John", "Doe", "john.doe@gmail.com")

    session.add(user)
    session.commit()


if __name__ == "__main__":
    main()
