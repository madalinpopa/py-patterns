# coding: utf-8

# aggregates/service.py

from model import Profile, register_user, register_user_profile
from unit_of_work import SqlAlchemyUnitOfWork


def create_profile(firstname: str, lastname: str, email: str):

    try:
        profile = register_user_profile(firstname, lastname, email)
        return profile
    except ValueError as err:
        print(f"ValueError: {err}")
    return None


def create_user(username: str, password: str, role: str, profile: Profile):

    try:
        user = register_user(username, password, role)
        user.profile = profile

        uow = SqlAlchemyUnitOfWork()

        with uow:
            uow.repo.add(user)

        return True
    except ValueError as err:
        print(f"ValueError: {err}")

    return False


def get_user_by_username(username: str):

    uow = SqlAlchemyUnitOfWork()
    user = None

    with uow:
        user = uow.repo.get_by_username(username)
    return user
