# coding: utf-8

# repository/repo.py

import abc
from typing import Any

from model import User, Profile


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, obj: Any) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Any:
        raise NotImplementedError


class UserRepository(AbstractRepository):
    pass
