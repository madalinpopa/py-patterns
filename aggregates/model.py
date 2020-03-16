# coding: utf-8

# aggregates/model.py


class Authentication:

    def __init__(self, password: str)
        self._user = User

    def hash_user_pass(self):
        pass

    def verify_user_pass(self):
        pass


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
