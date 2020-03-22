# coding: utf-8

# examples/demo.py


from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

# metadata
metadata = MetaData()

# define the engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define the session
session = sessionmaker(bind=engine)()


class User:
    def __init__(self, username, version=None):
        self._username = username
        self._version_uuid = version

    # @hybrid_property
    # def username(self):
    #     return self._username

    # @username.setter
    # def username(self, value):
    #     self._username = value


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("_username", String(30), nullable=False),
    Column("_version_id", String(32), nullable=False),
)


def start_mapper():
    mapper(
        User,
        user,
        order_by="user._username",
        version_id_col="_version_id",
        version_id_generator=lambda version: uuid.uuid4().hex,
    )


def main():

    start_mapper()

    metadata.create_all(bind=engine)

    user = User("madalin")
    session.add(user)
    session.commit()


if __name__ == "__main__":
    main()
