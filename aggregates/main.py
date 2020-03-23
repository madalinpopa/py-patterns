# coding: utf-8

import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import metadata, start_mapper

from service import create_profile, create_user, get_user_by_username

# define engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables

    metadata.create_all(bind=engine)

    # profile = create_profile("John", "Doe", "john.doe@gmail.com")
    # create_user("john", "secret", "admin", profile)

    user = get_user_by_username("john")
    print(user)


if __name__ == "__main__":
    main()
