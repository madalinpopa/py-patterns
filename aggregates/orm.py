# coding: utf-8

# aggregates/orm.py

from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship

from model import User, Role, UserAggregate


metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(30), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), nullable=False),
    Column("password", String(250), nullable=False),
)

user_agg = Table(
    "user_agg",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_number", Integer, nullable=False),
    Column("username", String(50), nullable=False),
)


def start_mapper():
    mapper(Role, role, properties={"user": relationship(User, back_populates="roles")})
    mapper(User, user, properties={"roles": relationship(Role, back_populates="user")})
    mapper(UserAggregate, user_agg)
