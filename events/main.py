# coding: utf-8

# events/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import metadata, start_mapper

from model import register_user
from unit_of_work import  SqlAlchemyUnitOfWork

# define engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    metadata.create_all(bind=engine)

    user = register_user("madalin", "password", "admin")

    uow = SqlAlchemyUnitOfWork()

    with uow:
        uow.repo.add(user)


if __name__ == "__main__":
    main()
