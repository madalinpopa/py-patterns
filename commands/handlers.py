# coding: utf-8

# commands/handlers.py

import command
import event
import model
import unit_of_work


def create_order(cmd: command.CreateNewOrder, uow: unit_of_work.AbstractUnitOfWork):
    try:
        order = model.create_order(cmd.firstname, cmd.lastname, cmd.country, cmd.city)
        with uow:
            uow.repo.add(order)
            return order
    except ValueError as err:
        print(f"ValueError: {err}")
    return None


def send_notification(
    evn: event.NotificationEvent, uow: unit_of_work.AbstractUnitOfWork
):
    print(f"Notification {evn.message}.")
