# coding: utf-8

# aggregates/repo.py

import abc

from model import User
from sqlalchemy.orm import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abc.abstractmehtod
    def get(self, username: str) -> User:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, user: User):
        self._session.add(user)

    def get(self, username: str) -> User:
        return self._session.query(User).filter_by(username=username).first()
