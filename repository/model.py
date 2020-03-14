# coding: utf-8

# repository/model.py


class Profile:
    def __init__(
        self, firstname: str, lastname: str, email: str, user_id=None, user=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.user_id = user_id
        self.user = user

    def __repr__(self):
        return f"<Profile: {self.firstname, self.lastname}>"


class User:
    def __init__(self, username: str, password: str, profile=None):
        self.username = username
        self.password = password
        self.profile = profile

    def __repr__(self):
        return f"<User: {self.username}>"
