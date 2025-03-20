import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_model import Base, User


def create_docker_postgresql_database_engine():
    """Create the postrgresql engine for the local docker postgresql.

    Most of the values are more or less hard coded.

    Returns
    -------
    sqlalchemy.engine.base.Engine
        An sqlalchmey Engine for the docker database
    """
    username = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "secret")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = "postgres"
    # This name is the same one used in the alembic.ini
    return create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
    )


def create_database(engine: sqlalchemy.engine.base.Engine):
    """Create database tables.

    Parameters
    ----------
    engine : sqlalchemy.engine.base.Engine
        The SQLite database engine to create the tables on.
    """
    Base.metadata.create_all(engine)


def delete_database(
    engine: sqlalchemy.engine.base.Engine, delete_database: bool = False
):
    """Delete database tables.

    Parameters
    ----------
    engine : sqlalchemy.engine.base.Engine
        The SQLite database engine to delete the tables from.
    delete_database : bool, optional
        Boolean flag specifying whether to actually delete the database or not, by default False.

    Raises
    ------
    ValueError
        If delete_database is False, raises ValueError with a warning message.
    """
    if not delete_database:
        raise ValueError(
            "delete_database is False. Are you sure you want to delete this database"
        )
    Base.metadata.drop_all(engine)


def add_test_data(engine):
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert data
    user1 = User(name="Alice", age=30)
    user2 = User(name="Bob", age=25)
    session.add_all([user1, user2])
    session.commit()
