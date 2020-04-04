# coding: utf-8

# events/messagebuss.py

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


def send_mail_notification_event(username: str, uow=None):
    print(f"Mail notification sent for {username} creation!")


HANDLERS = {
    event.UseCreationEvent: [send_mail_notification_event],
    event.NewUserEvent: [handlers.create_user],
}
