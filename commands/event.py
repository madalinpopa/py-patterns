# coding: utf-8

# commands/event.py

from dataclasses import dataclass
from typing import List

import model


class Event:
    pass


@dataclass
class NewOrderEvent(Event):
    firstname: str
    lastname: str
    country: str
    city: str


@dataclass
class NotificationEvent(Event):
    message: str
