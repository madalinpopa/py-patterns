# coding: utf-8

# aggregates/model.py

import binascii
import hashlib
import os
from typing import List


class UserManagement:
    def __init__(self, username: str, password: str, roles: List[str]):
        self.username = username
        self.password = password
        self.roles = roles


    def create_user

    def _hash_user_pass(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode("ascii")

    def _verify_user_pass(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 1000
        )
        pwdhash = binascii.hexlify(pwdhash).decode("ascii")
        return stored_password == pwdhash


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
