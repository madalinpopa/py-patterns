# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from orm import start_mapper, metadata
import uuid

from model import Email, Role, User, Profile, register_user, register_user_profile

# define engine
engine = create_engine("sqlite:///aggregate.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables

    metadata.create_all(bind=engine)

    user = register_user("madalin", "secret", "admin")
    profile = register_user_profile("Popa", "John", "test@gmail.com")
    session.add_all([user, profile])
    session.commit()
    user.profile = profile

    user_db = session.query(User).filter_by(username="madalin").first()
    profile_db = session.query(Profile).filter_by(firstname="Popa").first()

    print("User: ", user_db)
    print("Profile: ", profile_db)


if __name__ == "__main__":
    main()
