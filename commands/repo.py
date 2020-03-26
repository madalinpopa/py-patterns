# coding: utf-8

# commands/repo.py

import abc

import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, order: model.Order):
        self._add(order)
        self.seen.add(order)

    def get(self, reference: str):
        order = self._get(reference)
        if order:
            self.seen.add(order)
        return order

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

    def _add(self, order: model.Order):
        self.session.add(order)

    def _get(self, reference: str):
        return self.session.query(model.Order).filter_by(reference=reference).first()
