# coding: utf-8

# service/repo.py

import abc

from sqlalchemy.orm import Session

from model import Blog


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, blog: Blog):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, name: str) -> Blog:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, blog: Blog):
        self._session.add(blog)

    def get(self, name: str) -> Blog:
        return self._session.query(Blog).filter_by(name=name).first()
