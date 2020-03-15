# coding: utf-8

# aggregates/orm.py

from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship

from model import User, Profile

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(30), nullable=False),
    Column("password", String(250), nullable=False),
)

profile = Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstname", String(30), nullable=False),
    Column("lastname", String(30), nullable=False),
    Column("email", String(30), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)


def start_mapper():
    mapper(
        User, user, properties={"profile": relationship(Profile, back_populates="user")}
    )
    mapper(
        Profile,
        profile,
        properties={"user": relationship(User, back_populates="profile")},
    )

