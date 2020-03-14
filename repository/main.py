# coding: utf-8

# repository/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Profile, User
from orm import metadata, start_mapper

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

    session.add(user)
    session.add(profile)
    session.commit()

    user = session.query(User).filter_by(username="ed").first()
    profile = session.query(Profile).filter_by(firstname="John").first()

    user.profile = profile
    session.commit

    print("user.profile", user.profile)
    print("profile.user", profile.user)


if __name__ == "__main__":
    main()
