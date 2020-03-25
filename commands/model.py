# coding: utf-8

# commands/model.py

import abc
from sqlalchemy.ext.hybrid import hybrid_property

from typing import List
import uuid

def create_order(firstname: str, lastname: str, country: str, city: str, lines: List["Line"]) -> "Order":
    customer = Customer(firstname, lastname)
    addres = Address(country, city)
    reference = uuid.uuid4().hex
    order = Order(reference, customer, address, lines )
    order.events.append("event")
    return order


class Line:
    def __init__(self, sku: str, qty: int, price: int):
        self._sku = sku
        self._qty = qty
        self._price = price

    def __str__(self):
        return f"{self._sku}, {self._qty}"

    def __repr__(self):
        return f"Line(sku={self._sku}, qty={self._qty}, price={self._price})"

    def __eq__(self, other_line):
        if not isinstance(other_line, Line):
            return NotImplemented
        return self._sku == other_line._sku

    def __ne__(self, other_line):
        return not (self == other_line)

    def __hash__(self):
        return hash(self._sku)

    @property
    def sku(self):
        return self._sku

    @property
    def qty(self):
        return self._qty

    @property
    def price(self):
        return self._price

    def replace(self, sku=None, qty=None, price=None):
        line = Line(
            sku=sku or self._sku, qty=qty or self._qty, price=price or self._price
        )
        return line


class Customer:
    def __init__(self, firstname: str, lastname: str):
        self._firstname = firstname
        self._lastname = lastname

    def __str__(self):
        return f"{self._firstname} {self._lastname}"

    def __repr__(self):
        return f"Customer(firstname={self._firstname}, lastname={self._lastname})"

    def __eq__(self, other_customer):
        if not isinstance(other_customer, Customer):
            return NotImplemented
        return self._firstname == other_customer._firstname

    def __ne__(self, other_customer):
        return not (self == other_customer)

    def __hash__(self):
        return hash(self._firstname + self._lastname)

    @property
    def firstname(self):
        return self._firstname

    @property
    def lastname(self):
        return self._lastname


class Address:
    def __init__(self, country: str, city: str):
        self._country = country
        self._city = city

    def __str__(self):
        return f"{self._country}, {self._city}"

    def __repr__(self):
        return f"Address(country={self._country}, city={self._city})"

    def __eq__(self, other_address):
        if not isinstance(other_address, Address):
            raise NotImplemented
        return self._country == other_address._country

    def __ne__(self, other_address):
        return not (self == other_address)

    def __hash__(self):
        return hash(self._country + self._city)

    @property
    def country(self):
        return self._country

    @property
    def city(self):
        return self._city

    def replace(self, country=None, city=None):
        address = Address(country=country or self._country, city=city or self._city)
        return address


class Entity(abc.ABC):
    @abc.abstractmethod
    def __init__(self, reference: str):
        self._reference = reference
        self._version: str
        self.events = []

    @hybrid_property
    def reference(self):
        return self._reference

    @hybrid_property
    def version(self):
        return self._version


class Order(Entity):
    def __init__(self, reference: str, customer: Customer, address: Address, lines: List[Line]):
        super().__init__(reference)
        self._customer = customer
        self._address = address
        self._lines = lines

    def __str__(self):
        return f"Order: {self._reference}"

    def __repr__(self):
        return f"Order(reference={self._reference}, customer={self._customer})"

    @hybrid_property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, values: List[Line]):
        if len(values) < 1:
            raise ValueError("list of lines cannot be empty.")
        self._lines = value

    @hybrid_property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if not isinstance(value, Customer):
            raise ValueError(f"{value} is not instance of {Customer}")
        self._customer = value
    
    @hybrid_property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value):
        if not isinstance(value, Address):
            raise ValueError(f"{value} is not instance of {Address}")
        self._address = value

