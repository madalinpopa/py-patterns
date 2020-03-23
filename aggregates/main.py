# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from orm import start_mapper, metadata
import uuid

from model import Email, Role, User, Profile, register_user, register_user_profile

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
        user = uow.repo.get("e0fbd31932a54ed393c4fadef1a6e391")
        print(user)


if __name__ == "__main__":
    main()
