# coding: utf-8

# commands/event.py

from dataclasses import dataclass
from typing import List

import model


class Event:
    pass

@dataclass
class NewOrderEvent(Event):
    reference: str
    firstname: str
    lastname: str
    country: str
    city: str
    lines: List[model.Line]
