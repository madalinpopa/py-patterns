# coding: utf-8

# aggregates/orm.py

from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import mapper, relationship

from model import Email, User, Profile, Role


metadata = MetaData()

email = Table(
    "email",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("local_part", String(255), nullable=False),
    Column("domain_part", String(255), nullable=False),
    Column("profile_id", Integer, ForeignKey("profile.id")),
)

profile = Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("_uuid", String(100), nullable=False),
    Column("_version", Integer, nullable=False),
    Column("_discarded", Boolean, nullable=False),
    Column("_firstname", String(50), nullable=False),
    Column("_lastname", String(50), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("_name", String(30), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("_uuid", String(100), nullable=False),
    Column("_version", Integer, nullable=False),
    Column("_discarded", Boolean, nullable=False),
    Column("_username", String(50), nullable=False),
    Column("_password", String(255), nullable=False),
)


def start_mapper():
    mapper(
        Email,
        email,
        properties={
            "_profile": relationship(Profile, uselist=False, back_populates="_email")
        },
    )
    mapper(
        Profile,
        profile,
        properties={
            "_email": relationship(Email, uselist=False, back_populates="_profile"),
            "_user_profile": relationship(
                User, uselist=False, back_populates="_profile"
            ),
        },
    )
    mapper(
        Role,
        role,
        properties={"_user": relationship(User, uselist=False, back_populates="_role")},
    )
    mapper(
        User,
        user,
        properties={
            "_role": relationship(Role, uselist=False, back_populates="_user"),
            "_profile": relationship(
                Profile, uselist=False, back_populates="_user_profile"
            ),
        },
    )
