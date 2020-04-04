# coding: utf-8

# event_design/repo.py

import abc

from model import User


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, user: User):
        self._add(user)
        self.seen.add(user)

    def get(self, reference: str):
        user = self._get(reference)
        if user:
            self.seen.add(user)
        return user

    @abc.abstractmethod
    def _add(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self):
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, user: User):
        self.session.add(user)

    def _get(self, reference: str):
        return self.session.query(User).filter_by(reference=reference).first()
