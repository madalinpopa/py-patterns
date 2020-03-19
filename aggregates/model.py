# coding: utf-8

# aggregates/model.py

import binascii
import hashlib
import os
from typing import List

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.profile: Profile

    def __repr__(self):
        return f"<User: {self.username}>"


class Profile:
    def __init__(self, firstname: str, lastname: str, email: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.user: User

    def __repr__(self):
        return f"<Profile: {self.firstname} {self.lastname}>"


class UserAggregate:
    def __init__(self, username: str, version_number: int = 0):
        self._username = User()
        self.version_number = version_number
