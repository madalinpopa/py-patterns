# coding: utf-8


from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateNewOrder(Command):
    firstname: str
    lastname: str
    country: str
    city: str
