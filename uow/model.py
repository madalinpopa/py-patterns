# coding: utf-8

# uow/model.py

import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Line:
    order: int
    sku: str
    qty: int


class Order:
    def __init__(self, reference: str, customer: str, date=datetime.datetime.now()):
        self.reference = reference
        self.customer = customer
        self.date = date
        self.lines = []

    def __repr__(self):
        return f"<Order:{self.reference}>"
