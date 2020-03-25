# coding: utf-8

# commands/main.py

from sqlalchemy import create_engine

import event
import messagebus
import model
import unit_of_work
from orm import metadata, start_mapper

# engine
engine = create_engine("sqlite:///demo.db", echo=True)


def main():

    start_mapper()
    metadata.create_all(bind=engine)
    try:
        lines = [
            model.Line("Product 1", 10, 250),
            model.Line("Product 2", 23, 350),
            model.Line("Product 3", 14, 150),
        ]
        evn = event.NewOrderEvent(
            firstname="John", lastname="Doe", country="Romania", city="Bucharest",
        )

        uow = unit_of_work.SqlAlchemyUnitOfWork()
        result = messagebus.handle(evn, uow)
        print(result)
    except ValueError as err:
        print(ValueError)


if __name__ == "__main__":
    main()
