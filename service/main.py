# coding: utf-8

# service/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Blog, Post, Tag
from orm import metadata, start_mapper

from repo import SqlRepository
from unit_of_work import SqlAlchemyUnitOfWork


# define engine
engine = create_engine("sqlite:///service.db")

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables
    metadata.create_all(bind=engine)

    blog = Blog("myblog")

    post = Post("Post title")
    post.blog = blog

    tag = Tag("programming")
    tag.posts.append(post)

    # save
    uow = SqlAlchemyUnitOfWork()

    with uow:
        uow.repo.add(blog)
        uow.commit()


if __name__ == "__main__":
    main()
