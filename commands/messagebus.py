# coding: utf-8

# commands/messagebus.py

import logging
from typing import List, Union

import command
import event
import handlers
import unit_of_work

# define the logger
logger = logging.getLogger(__name__)

Message = Union[command.Command, event.Event]


def handle(message: Message, uow: unit_of_work.AbstractUnitOfWork):
    result = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, event.Event):
            handle_event(message, queue, uow)
        elif isinstance(message, command.Command):
            cmd_result = handle_command(message, queue, uow)
            result.append(cmd_result)
        else:
            raise Exception(f"{message} was not an Event or a Command")
    return result


def handle_event(
    evn: event.Event, queue: List[Message], uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(evn)]:
        try:
            logger.debug(f"handeling {evn} with handler {handler}")
            handler(evn, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception(f"Exception handling event {evn}")
            continue


def handle_command(
    cmd: command.Command, queue: List[Message], uow: unit_of_work.AbstractUnitOfWork
):
    logger.debug(f"handlin command {cmd}")
    try:
        handler = COMMAND_HANDLERS[type(cmd)]
        result = handler(cmd, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception(f"Exception handling {cmd}")
        raise


EVENT_HANDLERS = {event.NotificationEvent: [handlers.send_notification]}

COMMAND_HANDLERS = {command.CreateNewOrder: handlers.create_order}
