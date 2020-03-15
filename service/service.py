# coding: utf-8

# service/service.py

from unit_of_work import AbstractUnitOfWork
import model
from typing import List


def create_post(
    blog_name: str, post_title: str, tags: List[str], uow: AbstractUnitOfWork
):

    with uow:
        blog = uow.repo.get(name=blog_name)
        if not blog:
            blog = model.Blog(blog_name)
            uow.repo.add(blog)
        # create a post
        post = model.Post(post_title)
        post.blog = blog

        # create tags
        tag_list = [model.Tag(t) for t in tags]

        post.tags.extend(tag_list)

        # save post to blog
        uow.commit()
