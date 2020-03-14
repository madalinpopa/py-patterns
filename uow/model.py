# coding: utf-8

# uow/model.py

from dataclasses import dataclass

import datetime

@dataclass
class Line:
    order_id: str
    sku: str
    qty: str


class Order:

    def __init__(self, customer: str, date: datetime.datetime, lines: Line=None):
        self.customer = customer
        self.date = date
        self.lines = lines


    def __repr__(self):
        return f"<Order:{self.customer}>"

