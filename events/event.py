# coding: utf-8

# events/events.py

from dataclasses import dataclass


class Event:
    pass


@dataclass
class UseCreationEvent(Event):
    username: str
