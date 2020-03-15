# coding: utf-8

# service/model.py

import datetime
from typing import List


class Blog:
    def __init__(self, name: str):
        self.name = name
        self.posts: List[Post]

    def __repr__(self):
        return f"<Blog: {self.name}>"


class Post:
    def __init__(self, title: str):
        self.title = title
        self.blog: Blog
        self.tags: List[Tag]

    def __repr__(self):
        return f"<Post: {self.title}>"


class Tag:
    def __init__(self, desc: str):
        self.desc = desc
        self.posts: Post

    def __repr__(self):
        return f"<Tag: {self.desc}>"
