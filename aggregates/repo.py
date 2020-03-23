# coding: utf-8

# aggregates/repo.py

import abc
from typing import Any, List

from model import Profile, User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> Any:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    def add(self, user: User):
        self._session.add(user)

    def get(self, reference: str) -> User:
        return self._session.query(User).filter_by(reference=reference).first()

    def get_all(self) -> List[User]:
        return self._session.query(User).all()

    def get_by_username(self, username: str):
        return self._session.query(User).filter_by(username=username).first()
