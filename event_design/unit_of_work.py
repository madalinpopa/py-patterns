# coding: utf-8

# event_design/unit_of_work.py

import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repo import AbstractRepository, SqlRepository

# engine
engine = create_engine("sqlite:///demo.db")

# default session
DEFAULT_SESSION = sessionmaker(bind=engine, expire_on_commit=False)


class AbstractUnitOfWork(abc.ABC):

    repo = AbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def publish_events(self):
        for user in self.repo.seen:
            while self.repo.seen:
                if len(user.events) != 0:
                    event = user.events.pop(0)
                    handle(event)
                else:
                    break


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

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
