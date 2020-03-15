# coding: utf-8

# service/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Blog, Post, Tag
from orm import metadata, start_mapper

from repo import SqlRepository
from unit_of_work import SqlAlchemyUnitOfWork

from service import create_post # type: ignore


# define engine
engine = create_engine("sqlite:///service.db")

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables
    metadata.create_all(bind=engine)

    # initiate uow
    uow = SqlAlchemyUnitOfWork()

    # user service
    create_post("My Blog", "Post 1", ["python", "programming"], uow)

    with uow:
        blog = uow.repo.get("My Blog")
        print("blog", blog)
        print("posts", blog.posts)
        print("Post 1, tags", blog.posts[0].tags)


if __name__ == "__main__":
    main()
