# coding: utf-8

# events/messagebuss.py

import event


def handle(evn: event.Event):
    for handler in HANDLERS[type(evn)]:
        handler(evn)


def send_mail_notification_event(username: str):
    print(f"Mail notification sent for {username} creation!")


HANDLERS = {event.UseCreationEvent: [send_mail_notification_event]}
