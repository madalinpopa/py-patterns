# code: utf-8

# events/service.py

from model import User, register_user
from unit_of_work import SqlAlchemyUnitOfWork


def create_user(username: str, password: str, role: str):
    try:
        user = register_user(username, password, role)

        uow = SqlAlchemyUnitOfWork()

        with uow:
            uow.repo.add(user)

        return True
    except ValueError as err:
        print(f"ValueError: {err}")
    return False
