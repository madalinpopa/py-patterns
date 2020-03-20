# coding: utf-8

# aggregates/model.py

import binascii
import hashlib
import os
from typing import List
from dataclasses import dataclass
import abc




class Role:  # value set
    name: str
    user: int


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.roles: List[Role]


class UserAggregate:
    def __init__(self, username: str, version_number: int = 0):
        self.username = username,
        self.version_number = version_number





