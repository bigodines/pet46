from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


def init_db(database_url):
    """
    Initialize the database engine and session factory.
    """
    engine = create_engine(database_url, echo=True)  # Set echo=False in production
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session()
