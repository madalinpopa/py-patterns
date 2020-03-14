# coding: utf-8

# repository/orm

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from .model import Profile, User

metadata = MetaData()

profile = Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstname", String(50), nullable=False),
    Column("lastname", String(50), nullable=False),
    Column("email", String("50"), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(30), nullable=False),
    Column("password", String(250), nullable=False),
)


def start_mapper():
    mapper(
        Profile,
        profile,
        properties={"user": relationship(User, uselist=False, backref="user")},
    )
    mapper(User, user, properties={"profile": relationship(Profile, backref="profile")})
