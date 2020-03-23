# coding: utf-8

import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Email, Profile, Role, User, register_user, register_user_profile
from orm import metadata, start_mapper
from unit_of_work import SqlAlchemyUnitOfWork

# define engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables

    metadata.create_all(bind=engine)

    user = register_user("madalin", "secret", "admin")
    profile = register_user_profile("Popa", "John", "test@gmail.com")
    user.profile = profile

    uow = SqlAlchemyUnitOfWork()

    # with uow:
    #     uow.repo.add(user)

    with uow:
        user = uow.repo.get("d0925fdeb72849c38c55260e08b2d59d")
        print(user.profile)


if __name__ == "__main__":
    main()
