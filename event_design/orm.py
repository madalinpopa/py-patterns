# coding: utf-8


# event_design/orm.py


import uuid

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from model import Role, User

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
    Column("reference", String(32), nullable=False),
    Column("version", String(32), nullable=False),
    Column("username", String(50), nullable=False),
    Column("password", String(50), nullable=False),
)


def start_mapper():
    mapper(
        Role,
        role,
        properties={
            "_name": role.c.name,
            "_user": relationship(User, uselist=False, back_populates="_role"),
        },
    )
    mapper(
        User,
        user,
        order_by=user.c.username,
        version_id=user.c.version,
        version_id_generator=lambda version: uuid.uuid4().hex,
        properties={
            "_reference": user.c.reference,
            "_version": user.c.version,
            "_username": user.c.username,
            "_password": user.c.password,
            "_role": relationship(Role, uselist=False, back_populates="_user"),
        },
    )
