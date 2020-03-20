# coding: utf-8


# examples/customer_entity.py

from entity import Entity
import uuid


class Customer(Entity):
    def __init__(self, customer_id, customer_version, name):
        """ DO NOT CALL DIRECTLY to create a new Customer. """
        super().__init__(customer_id, customer_version)
        self._name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(discarded={self._discarded}name={self_name}, id={self.id})"

    @property
    def name(self):
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value):
        self._check_not_discarded()
        if len(value) < 1:
            raise ValueError("Customer name cannot be empty")
        self._name = value
        self._increment_version()

    def register_customer(name):
        customer = Customer(customer_id=uuid.uuid4().hex, customer_version=0, name=name)
        return customer
