# coding: utf-8

# repository/model.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    firstname: str
    lastname: str
    email: str
    user: User


class User:
    def __init__(self, username: str, password: str, profile: Profile = None):
        self.username = username
        self.password = password
        self.profile = profile
