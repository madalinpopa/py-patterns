# coding: utf-8

# event_design/main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import event
import messagebuss
import unit_of_work
from orm import metadata, start_mapper

# define engine
engine = create_engine("sqlite:///demo.db", echo=True)

# define session
session = sessionmaker(bind=engine)()


def main():

    start_mapper()
    metadata.create_all(bind=engine)
    try:
        evn = event.NewUserEvent("john", "secret", "admin")
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        result = messagebuss.handle(evn, uow)
    except ValueError:
        pass


if __name__ == "__main__":
    main()
