# coding: utf-8

# event_design/events.py

from dataclasses import dataclass


class Event:
    pass


@dataclass
class UseCreationEvent(Event):
    username: str
