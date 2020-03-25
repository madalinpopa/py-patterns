# coding: utf-8

# commands/event.py

from dataclasses import dataclass

class Event:
    pass

@dataclass
class NewOrderEvent(Event):
    reference: str
    customer: str