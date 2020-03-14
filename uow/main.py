# coding: utf-8

# uow/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Line, Order
from orm import metadata, start_mapper

from repo import SqlRepository

from unit_of_work import SqlAlchemyUnitOfWork


# define engine
engine = create_engine("sqlite:///uow.db")

# create session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()

    # create all the tables
    metadata.create_all(bind=engine)

    order = Order("ORD-1", "John Doe")
    line1 = Line(order, "Product-1", 10)
    line2 = Line(order, "Product-2", 20)
    line3 = Line(order, "Product-3", 12)

    # save
    uow = SqlAlchemyUnitOfWork()

    with uow:
        uow.repo.add(order)
        uow.commit()

    with uow:
        order = uow.repo.get("ORD-1")
        print(order.lines)


if __name__ == "__main__":
    main()
