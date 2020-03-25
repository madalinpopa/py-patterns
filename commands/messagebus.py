# coding: utf-8

# commands/messagebus.py

import event
import handlers
import unit_of_work

def handle(evn: event.Event, uow: unit_of_work.AbstractUnitOfWork):
    result = []
    queue = [evn]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            result.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())
    return result


HANDLERS = {
    event.NewOrderEvent: [handlers.create_order]
}