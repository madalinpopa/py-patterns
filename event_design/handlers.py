# coding: utf-8


# events_design/service


import event
from model import User, register_user
from unit_of_work import AbstractRepository


def create_user(evn: event.NewUserEvent, uow: AbstractRepository):
    try:
        user = register_user(evn.username, evn.password, evn.role)
        with uow:
            uow.repo.add(user)
        return True
    except ValueError as err:
        print(f"ValueError: {err}")
    return False
