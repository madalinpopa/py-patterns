# coding: utf-8

# uow/model.py

from sqlalchemy import MetaData, Table, ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import mapper, relationship

from model import Line, Order

import datetime

metadata = MetaData()

line = Table(
    "line",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("sku", String(50), nullable=False),
    Column("qty", Integer, nullable=False),
)

order = Table(
    "order",
    Order,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("customer", String(50), nullable=True),
    Column("date", Date, default=datetime.datetime.now()),
)


def start_mapper():
    mapper(Order, order, properties={"lines": relationship(Line, backref="line.id")})
    mapper(
        line, Line, properties={"lines": relationship(Order, back_populates="lines")}
    )

