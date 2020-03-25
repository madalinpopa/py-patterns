# coding: utf-8

# commands/handlers.py

import event
import model
import unit_of_work


def create_order(evn: event.NewOrderEvent, uow: unit_of_work.AbstractRepository):
    try:
        order = model.create_order(evn.firstname, evn.lastname, evn.country, evn.city)
        with uow:
            uow.repo.add(order)
            return order
    except ValueError as err:
        print(f"ValueError: {err}")
    return None
