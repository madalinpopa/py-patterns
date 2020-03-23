# coding: utf-8

# service/orm.py

import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from model import Blog, Post, Tag

metadata = MetaData()

blog = Table(
    "blog",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
)

post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(50), nullable=False),
    Column("date", Date, default=datetime.datetime.now()),
    Column("blog.id", Integer, ForeignKey("blog.id")),
)

tag = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("desc", String(30), nullable=True),
)

tag_post = Table(
    "tag_post",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


def start_mapper():
    mapper(
        Blog, blog, properties={"posts": relationship(Post, back_populates="blog")},
    )
    tag_mapp = mapper(
        Tag,
        tag,
        properties={
            "posts": relationship(Post, secondary=tag_post, back_populates="tags")
        },
    )
    mapper(
        Post,
        post,
        properties={
            "blog": relationship(Blog, uselist=False, back_populates="posts"),
            "tags": relationship(tag_mapp, secondary=tag_post, back_populates="posts"),
        },
    )
