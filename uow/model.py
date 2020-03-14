# coding: utf-8

# uow/model.py

import datetime
from dataclasses import dataclass


@dataclass
class Line:
    order_id: int
    sku: str
    qty: str


class Order:
    def __init__(
        self, reference: str, customer: str, date: datetime.datetime, lines: Line = None
    ):
        self.reference = reference
        self.customer = customer
        self.date = date
        self.lines = lines

    def __repr__(self):
        return f"<Order:{self.customer}>"
