# coding: utf-8

# aggregates/model.py

import abc
import uuid
from typing import Any, List, NewType

from sqlalchemy.ext.hybrid import hybrid_property


# Factory function
def register_user(username: str, password: str, role: str):
    user_role = Role(role)
    user_id = uuid.uuid4().hex
    user = User(user_id=user_id, username=username, password=password, role=user_role)
    return user


def register_user_profile(firstname: str, lastname: str, email: str):
    email_address = Email.from_text(email)
    profile_id = uuid.uuid4().hex
    profile = Profile(
        profile_id=profile_id,
        firstname=firstname,
        lastname=lastname,
        email=email_address,
    )
    return profile


# Exceptions


class DiscardEntityError(Exception):
    """ Raised when an attempt is made to use a discarded entity. """


# Value Objects


class Email:
    """ Email value object. """

    @classmethod
    def from_text(cls, address):
        if "@" not in address:
            raise ValueError("Email address must contain '@'")
        local_part, _, domain_part = address.partition("@")
        return cls(local_part, domain_part)

    def __init__(self, local_part: str, domain_part: str):
        if len(local_part) + len(domain_part) > 255:
            raise ValueError("Email address too long")
        self._local_part = local_part
        self._domain_part = domain_part
        self._profile: "Profile"  # this is assigned automatically

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

    def __init__(self, name: str):
        self._name = name
        self._user: "User"  # this will be assigned automatically

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


# Entities


class Entity(abc.ABC):
    """ 
    Base entity class for all entities.
    
    reference: A unique identifier
    instance_id: A value unique among instances of this entity
    version: A value unique for each changes, modification
    discarded: True if this entity should or not longer be used
    
    """

    @abc.abstractmethod
    def __init__(self, reference_id: str):
        self._id = reference_id
        self._version: str

    @hybrid_property
    def reference(self) -> str:
        return self._id

    @hybrid_property
    def version(self) -> int:
        return self._version


class Profile(Entity):
    """ Profile Aggregate Entity. """

    def __init__(self, profile_id: str, firstname: str, lastname: str, email: Email):
        super().__init__(profile_id)
        self._firstname = firstname
        self._lastname = lastname
        self._email = email
        self._user_profile: int  # this is assigned when the user is created

    def __str__(self):
        return f"{self._firstname} {self._lastname}"

    def __repr__(self):
        return f"Profile(id={self._id}, firstname={self._firstname}, lastname={self._lastname})"

    @hybrid_property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        if len(value) < 1:
            raise ValueError("First Name cannot be empty")
        self._firstname = value

    @hybrid_property
    def lastname(self):
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        if len(value) < 1:
            raise ValueError("Last Name cannot be empty")
        self._lastname = value

    @hybrid_property
    def user_profile(self):
        return self._user_profile

    @user_profile.setter
    def user_profile(self, value):
        if not isinstance(value, User):
            raise ValueError(f"{value} is not instance of {User}")
        self._user_profile = value

    @hybrid_property
    def email(self):
        self._check_not_discarded()
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, Email):
            raise ValueError(f"{value} is not instance of {Email}")
        self._email = value


class User(Entity):
    """ User Root Aggregate. """

    def __init__(self, user_id: str, username: str, password: str, role: Role):
        super().__init__(user_id)
        self._username = username
        self._password = password
        self._role = role
        self._discarded = False
        self._profile: int  # This is assigned automatically when assign profile

    def __repr__(self):
        return f"User(reference={self._id}, username={self._username})"

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if len(value) < 1:
            raise ValueError("Username cannot be empty.")
        self._username = value

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        if len(value) < 1:
            raise ValueError("Password cannot be empty")
        self._password = value
        self._increment_version

    @hybrid_property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        if not isinstance(value, Profile):
            raise ValueError(f"{value} is not instance of {Profile}")
        self._profile = value

    @hybrid_property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, Role):
            raise ValueError(f"{value} is not instance of {Role}")
        self._role = value
