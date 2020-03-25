# coding: utf-8

# commands/orm.py

import uuid

from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, relationship

import model

metadata = MetaData()

line = Table(
    "line",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(30), nullable=False),
    Column("qty", Integer, nullable=False),
    Column("price", Integer, nullable=False),
    Column("order_id", Integer, ForeignKey("order.id")),
)

customer = Table(
    "customer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstname", String(50), nullable=False),
    Column("lastname", String(50), nullable=False),
    Column("cust_order_id", Integer, ForeignKey("order.id")),
)

address = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("country", String(50), nullable=False),
    Column("city", String(50), nullable=False),
    Column("addr_order_id", Integer, ForeignKey("order.id")),
)

order = Table(
    "order",
    metadata, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(32), nullable=False),
    Column("version", String(32), nullable=False),
)

def start_mapper():
    """ Maper function """
    mapper(
        model.Line, 
        line,
        properties={
            "_sku": line.c.sku,
            "_qty": line.c.qty,
            "_price": line.c.price,
            "order_id": relationship(model.Order, back_populates="lines")
        }
    )
    mapper(
        model.Customer,
        customer,
        properties={
            "_firstname": customer.c.firstname,
            "_lastname": customer.c.lastname,
            "cust_order_id": relationship(model.Order, uselist=False, back_populates="_customer")
        }
    )
    mapper(
        model.Address,
        address,
        properties={
            "_country": address.c.country,
            "_city": address.c.city,
            "addr_order_id": relationship(model.Order, uselist=False, back_populates="_address")
        }
    )
    mapper(
        model.Order,
        order,
        version_id_col=order.c.version,
        version_id_generator=lambda version: uuid.uuid4().hex,
        properties={
            "_reference": order.c.reference,
            "_version": order.c.version,
            "_customer": relationship(model.Customer, uselist=False, back_populates="cust_order_id"),
            "_address": relationship(model.Address, uselist=False, back_populates="addr_order_id"),
            "_lines": relationship(model.Line, uselist=False, back_populates="order_id")
        }
    )