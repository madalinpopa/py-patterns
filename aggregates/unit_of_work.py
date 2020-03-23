# coding: utf-8

# aggregates/uow.py

import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repo import AbstractRepository, SqlRepository

DEFAULT_SESSION = sessionmaker(bind=create_engine("sqlite:///demo.db"))


class AbstractUnitOfWork(abc.ABC):

    repo = AbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()

    @abc.abstractmethod
    def commit():
        raise NotImplementedError

    @abc.abstractmethod
    def rollback():
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = SqlRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
