# coding: utf-8

# repository/repo.py

import abc
from typing import Any, List

from sqlalchemy.orm import Session

from model import Profile, User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, obj: Any) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: Any) -> Any:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, user: User) -> None:
        self._session.add(user)

    def get(self, username: str) -> User:
        return self._session.query(User).filter_by(username=username).first()

    def get_all_users(self) -> List[User]:
        return self._session.query(User).all()
