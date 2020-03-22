# coding: utf-8

# aggregates/model.py

import abc
import binascii
import hashlib
import os
import uuid
from dataclasses import dataclass
from typing import Any, List, NewType

from sqlalchemy.ext.hybrid import hybrid_property
import uuid

# Custom Types

name = NewType("Name", str)
username = NewType("Username", str)


# Exceptions


class DiscardEntityError(Exception):
    """ Raised when an attempt is made to use a discarded entity. """


# Entities


class Entity(abc.ABC):
    """ Base entity class for all entities. """

    @abc.abstractmethod
    def __init__(self, uuid_id: str, version: int = 0):
        self._uuid = uuid_id
        self._version = version
        self._discarded = False
        self._instance_id = uuid.uuid4().hex

    @hybrid_property
    def uuid() -> str:
        self._check_not_discarded()
        return self._uuid

    @hybrid_property
    def version(self) -> int:
        self._check_not_discarded
        return self._version

    @hybrid_property
    def discarded(self) -> bool:
        return self._discarded

    @hybrid_property
    def instance_id(self) -> str:
        return self._instance_id

    def increment_version(self) -> None:
        self._version += 1

    def _check_not_discarded(self) -> None:
        if self._discarded:
            raise DiscardEntityError(f"Attempt to use {self.__class__.__name__}")


# Value Objects


class Email:
    """ Email value object. """

    @classmethod
    def from_text(cls, address):
        if "@" not in address:
            raise ValueError("Email address must contain '@'")
        local_part, _, domain_part = address.partition("@")
        self._local_part = local_part
        self._domain_part = domain_part

    def __init__(self, local_part: str, domain_part: str, profile: "Profile"):
        if len(local_part) + len(domain_part) > 255:
            raise ValueError("Email address too long")
        self._local_part = local_part
        self._domain_part = domain_part
        self._profile = profile

    def __str__(self):
        return "@".join(self._domain_part)

    def __repr__(self):
        return f"Email(local_part={self._local_part}, domain_part={self._domain_part})"

    def __eq__(self, email_obj: Any):
        if not isinstance(email_obj, Email):
            return NotImplemented
        return self._local_part == email_obj._local_part

    def __ne__(self, email_obj: Any):
        return not (self == email_obj)

    def __hash__(self):
        return hash(self._local_part + self._domain_part)

    @hybrid_property
    def profile(self):
        return self._profile

    @hybrid_property
    def local(self):
        return self._local_part

    @hybrid_property
    def domain(self):
        return self._domain_part

    def replace(self, local=None, domain=None, profile=None):
        if not isinstance(profile, Proile):
            raise ValueError(f"{profile} is not instance of {Profile}")
        return Email(
            local_part=local or self._local_part,
            domain_part=domain or self._domain_part,
            profile=profile or self._profile,
        )


class Role:
    """ Role value object. """

    def __init__(self, name: str, user: "User"):
        self._name = name
        self._user = user

    def __str__(self):
        return f"name={self._name}"

    def __repr__(self):
        return f"Role(name={self._name})"

    def __eq__(self, obj: Any):
        if not isinstance(obj, Role):
            return NotImplemented
        return self._name == obj._name

    def __ne__(self, obj):
        return not (self == obj)

    def __hash__(self):
        return hash(self._name)

    @hybrid_property
    def name(self) -> str:
        return self._name

    @hybrid_property
    def user(self):
        return self._user

    def replace(self, name=None, user=None):
        if not isinstance(user, User):
            raise ValueError(f"{user} is not instance of {User}")
        return Role(name=name or self._name, user=user or self._user)


class Profile(Entity):
    """ Profile Aggregate Entity. """

    def __init__(
        self, profile_id: str, profile_version: int = 0, firstname=None, lastname=None
    ):
        super().__init__(profile_id, profile_version)
        self._firstname = firstname
        self._lastname = lastname
        self._user_profile: int
        self._email: int

    def __repr__(self):
        return f"Profile(id={self.uuid}, version={self.version}, firstname={self._firstname}, lastname={self._lastname})"

    @hybrid_property
    def firstname(self):
        self._check_not_discarded()
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("First Name cannot be empty")
        self._firstname = value
        self._increment_version()

    @hybrid_property
    def lastname(self):
        self._check_not_discarded()
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Last Name cannot be empty")
        self._lastname = value
        self._increment_version()

    @hybrid_property
    def user_profile(self):
        self._check_not_discarded()
        return self._user_profile

    @user_profile.setter
    def user_profile(self, value):
        self._check_not_discarded()
        if not isinstance(value, User):
            raise ValueError(f"{value} is not instance of {User}")
        self._increment_version()
        self._user_profile = value

    @hybrid_property
    def email(self):
        self._check_not_discarded()
        return self._email

    @email.setter
    def email(self, value):
        self._check_not_discarded()
        if not isinstance(value, Email):
            raise ValueError(f"{value} is not instance of {Email}")
        self._email = value
        self._increment_version()

    def register_profile(self, firstname: str, lastname: str):
        profile = Profile(
            profile_id=uuid.uuid4().hex, firstname=firstname, lastname=lastname
        )
        return profile


class User(Entity):
    """ User Root Aggregate. """

    def __init__(
        self, user_id: str, user_version: int = 0, username=None, password=None
    ):
        super().__init__(user_id, user_version)
        self._username = username
        self._password = password
        self._profile: int
        self._role: int

    @hybrid_property
    def username(self):
        self._check_not_discarded()
        return self._username

    @username.setter
    def username(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Username cannot be empty.")
        self._username = value
        self._increment_version()

    @hybrid_property
    def password(self):
        self._check_not_discarded()
        return self._password

    @password.setter
    def password(self, value: str):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Password cannot be empty")
        self._password = value
        self._increment_version

    @hybrid_property
    def profile(self):
        self._check_not_discarded()
        return self._profile

    @profile.setter
    def profile(self, value):
        self._check_not_discarded()
        if not isinstance(value, Profile):
            raise ValueError(f"{value} is not instance of {Profile}")
        self._profile = value
        self._increment_version()

    @hybrid_property
    def role(self):
        self._check_not_discarded()
        return self._role

    @role.setter
    def role(self, value):
        self._check_not_discarded()
        if not isinstance(value, Role):
            raise ValueError(f"{value} is not instance of {Role}")
        self._role = value
        self._increment_version()

    def register_user(self, username: str, password: str):
        return User(user_id=uuid.uuid4().hex, username=username, password=password)
