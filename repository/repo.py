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


class UserRepository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, user: User) -> None:
        self._session.add(user)
        self._session.commit()
        self._session.flush()

    def get(self, username: str) -> User:
        return self._session.query(User).filter_by(username=username).first()

    def get_all_users(self) -> List[User]:
        return self._session.query(User).all()


class ProfileRepository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, profile: Profile) -> None:
        self._session.add(profile)
        self._session.commit()
        self._session.flush()

    def get(self, user_id: int) -> Profile:
        return self._session.query(Profile).filter_by(user_id=user_id).first()

    def get_all_profiles(self) -> List[Profile]:
        return self._session.query(Profile).all()
