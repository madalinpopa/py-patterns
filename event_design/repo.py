# coding: utf-8


# event_design/repo.py

import abc

from model import User


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, user: User):
        self._add(user)
