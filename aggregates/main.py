# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from orm import start_mapper, metadata
import uuid

from model import Email, Role, User, Profile

# define engine
engine = create_engine("sqlite:///aggregate.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables

    metadata.create_all(bind=engine)

    profile = Profile(uuid.uuid4().hex, 0)
    new = profile.register_profile(firstname="Popa", lastname="Madalin")
    user = User(uuid.uuid4().hex, 0)
    u1 = user.register_user("username", "password")
    session.add(u1)
    session.commit()
    print(u1)


if __name__ == "__main__":
    main()
