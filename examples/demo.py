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
    def __init__(self, username: str):
        self._username = username
        self._version: str

    @hybrid_property
    def version(self):
        return self._version

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    def __repr__(self):
        return f"{self._username}"


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(30), nullable=False),
    Column("version", String(32)),
)


def start_mapper():
    mapper(
        User,
        user,
        order_by=user.c.username,
        version_id_col=user.c.version,
        version_id_generator=lambda version: uuid.uuid4().hex,
        properties={"_username": user.c.username, "_version": user.c.version},
    )


def main():

    start_mapper()

    metadata.create_all(bind=engine)

    user = User("abmadalin")
    session.add(user)
    session.commit()


if __name__ == "__main__":
    main()
