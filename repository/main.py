# coding: utf-8

# repository/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Profile, User
from orm import metadata, start_mapper
from repo import AbstractRepository, SqlRepository

# define engine
engine = create_engine("sqlite:///repo.db", echo=True)

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all tables
    metadata.create_all(bind=engine)

    # initiate repository
    user_repo = SqlRepository(session)

    user = User("ed", "secret")
    profile = Profile("John", "Doe", "john.doe@gmail.com")

    user.profile = profile

    # add user and profile to database
    user_repo.add(user)

    # save
    session.commit()

    # query database
    user = user_repo.get(username="ed")

    print(user, user.profile)


if __name__ == "__main__":
    main()
