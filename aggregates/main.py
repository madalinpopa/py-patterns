# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from orm import start_mapper, metadata

# define engine
engine = create_engine("sqlite:///aggregate.db")

# define session
session = sessionmaker(bind=engine)


def main():

    start_mapper()

    # create all the tables
    
    metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()