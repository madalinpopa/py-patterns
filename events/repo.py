# coding: utf-8

# events/repo.py


import abc
from typing import Any

from model import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: Any):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str):
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    def add(self, user: User):
        self._session.add(user)

    def get(self, reference: str):
        self._session.query(User).filter_by(reference=reference).first()
