# coding: utf-8

# event_design/model.py


import abc
import uuid

from sqlalchemy.ext.hybrid import hybrid_property


def register_user(username: str, password: str, role: str):
    pass


class Role:
    def __init__(self, name: str):
        self._name = name
        self._user: "User"  # this will be assigned automatically

    def __str__(self):
        return f"Role name={self._name}"

    def __repr__(self):
        return f"Role(name={self._name})"

    def __eq__(self, other_role):
        if not isinstance(other_role, Role):
            return False
        return self.name == other_role._name

    def __ne__(self, other_role):
        return not (self == other_role)

    def __hash__(self):
        return hash(self._name)

    @hybrid_property
    def name(self):
        return self._name

    def update(self, value):
        if len(value) < 1:
            raise ValueError("Role name cannot be empty")
        return Role(name=value)


class Entity(abc.ABC):
    @abc.abstractmethod
    def __init__(self, reference: str):
        self._reference = reference
        self._version: str

    @hybrid_property
    def reference(self):
        return self._reference

    @hybrid_property
    def version(self):
        return self._version


class User(Entity):
    def __init__(self, reference: str, username: str, password: str, role: Role):
        super().__init__(reference)
        self._username = username
        self._password = password
        self._role = role

    def __str__(self):
        return f"{self._username}"

    def __repr__(self):
        return f"User(username={self._username})"

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if len(value) < 1:
            raise ValueError("username cannot be empty")
        self._username = value

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) < 1:
            raise ValueError("password field cannot be empty")
        self._password = value

    @hybrid_property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, Role):
            raise ValueError(f"{value} is not instance of {Role}")
