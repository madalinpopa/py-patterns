# coding: utf-8

# uow/model.py

import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from model import Line, Order

metadata = MetaData()

# child
line = Table(
    "line",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("sku", String(50), nullable=False),
    Column("qty", Integer, nullable=False),
)

# parent
order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(15), nullable=False, unique=True),
    Column("customer", String(50), nullable=True),
    Column("date", Date, default=datetime.datetime.now()),
)


def start_mapper():
    mapper(
        Order, order, properties={"lines": relationship(Line, back_populates="order")}
    )
    mapper(
        Line, line, properties={"order": relationship(Order, back_populates="lines")}
    )
