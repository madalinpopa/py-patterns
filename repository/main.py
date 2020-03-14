# coding: utf-8

# repository/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Profile, User
from orm import metadata, start_mapper
from repo import AbstractRepository, ProfileRepository, UserRepository

# define engine
engine = create_engine("sqlite:///repo.db", echo=True)

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all tables
    metadata.create_all(bind=engine)

    user = User("ed", "secret")
    profile = Profile("John", "Doe", "john.doe@gmail.com")

    user_repo = UserRepository(session)
    user_repo.add(user)

    profile_repo = ProfileRepository(session)
    profile_repo.add(profile)

    user.profile = profile

    user = user_repo.get("ed")
    profile = profile_repo.get(user.id)

    print(user, profile)


if __name__ == "__main__":
    main()
