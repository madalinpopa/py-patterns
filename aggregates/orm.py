# coding: utf-8

# aggregates/orm.py

import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from model import Email, Profile, Role, User

metadata = MetaData()

email = Table(
    "email",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("local_part", String(150), nullable=False),
    Column("domain_part", String(150), nullable=False),
    Column("profile_id", Integer, ForeignKey("profile.id")),
)

profile = Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(32), nullable=False),
    Column("version", Integer, nullable=False),
    Column("firstname", String(50), nullable=False),
    Column("lastname", String(50), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

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
    Column("version", Integer, nullable=False),
    Column("username", String(50), nullable=False),
    Column("password", String(255), nullable=False),
)


def start_mapper():
    mapper(
        Email,
        email,
        order_by=email.c.local_part,
        properties={
            "_local_part": email.c.local_part,
            "_domain_part": email.c.domain_part,
            "_profile": relationship(Profile, uselist=False, back_populates="_email"),
        },
    )
    mapper(
        Profile,
        profile,
        order_by=profile.c.firstname,
        version_id_col=profile.c.version,
        version_id_generator=lambda version: uuid.uuid4().hex,
        properties={
            "_id": profile.c.reference,
            "_version": profile.c.version,
            "_firstname": profile.c.firstname,
            "_lastname": profile.c.lastname,
            "_email": relationship(Email, uselist=False, back_populates="_profile"),
            "_user_profile": relationship(
                User, uselist=False, back_populates="_profile"
            ),
        },
    )
    mapper(
        Role,
        role,
        order_by=role.c.name,
        properties={
            "_name": role.c.name,
            "_user": relationship(User, uselist=False, back_populates="_role"),
        },
    )
    mapper(
        User,
        user,
        order_by=user.c.username,
        version_id_col=user.c.version,
        version_id_generator=lambda version: uuid.uuid4().hex,
        properties={
            "_id": user.c.reference,
            "_version": user.c.version,
            "_username": user.c.username,
            "_password": user.c.password,
            "_role": relationship(Role, uselist=False, back_populates="_user"),
            "_profile": relationship(
                Profile, uselist=False, back_populates="_user_profile"
            ),
        },
    )
