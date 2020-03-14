# coding: utf-8

# uow/repo.py

import abc
from typing import List

from model import Order


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, order: Order) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> Order:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    def add(self, order: Order) -> None:
        self._session.add(order)

    def get(self, reference: str) -> Order:
        return self._session.query(Order).filter_by(reference=reference).first()

    def get_all_orders(self) -> List[Order]:
        return self._session.query(Order).all()
