# coding: utf-8

# aggregates/model.py

import abc
import binascii
import hashlib
import os
import uuid
from dataclasses import dataclass
from typing import List, Any, NewType

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
    def __init__(id: str, version: str):
        self._id = id
        self._version = version
        self._discarded = False
        self._instance_id = uuid.uuid5()

    @property
    def id() -> str:
        self._check_not_discarded()
        return self._id

    @property
    def version(self) -> int:
        self._check_not_discarded
        return self._version

    @property
    def discarded(self) -> bool:
        return self._discarded

    @property
    def instance_id(self) -> str:
        return self._instance_id

    def increment_version(self) -> None:
        self._version += 1

    def _check_not_discarded(self) -> None:
        if self._discarded:
            raise DiscardEntityError(f"Attempt to use {self.__class__.__name__}")


# Value Objects


class Role:
    """ A user role. """

    def __init__(self, name: str):
        self._name = name

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

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name) -> "Role":
        return Role(name=new_name)


class User(Entity):
    """ User root Entity. """

    def __init__(self, user_id: str, user_version: str, username: str):
        super().__init__(user_id, user_version)
        self._id = user_id
        self._version = user_version
        self._username = username