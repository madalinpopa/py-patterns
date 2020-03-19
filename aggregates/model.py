# coding: utf-8

# aggregates/model.py


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
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = self._hash_password(password)
        self.user = User(self.username, self._password)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, uname):
        self._username = uname

    @property
    def password(self)

    def _hash_password(self, password):
        return f"hash +{password}" 

