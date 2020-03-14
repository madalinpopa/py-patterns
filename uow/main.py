# coding: utf-8

# uow/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Line, Order
from orm import metadata, start_mapper

from repo import SqlRepository


# define engine
engine = create_engine("sqlite:///uow.db")

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables
    metadata.create_all(bind=engine)

    # initiate repository
    repo = SqlRepository(session)

    order = Order("ORD-1", "John Doe")
    line1 = Line(order, "Product-1", 10)
    line2 = Line(order, "Product-2", 20)
    line3 = Line(order, "Product-3", 12)

    # add order
    repo.add(order)

    # save
    session.commit()

    order = repo.get("ORD-1")
    print(order.lines)


if __name__ == "__main__":
    main()
