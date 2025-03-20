import subprocess
from pathlib import Path

import click


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
LOCAL = Path(__file__).parent.resolve()
REPO_ROOT = Path(__file__).parent.parent.resolve()
DOCKER_COMPOSE_TEST = LOCAL / "docker-compose.test.yml"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """Container group for all commands."""
    pass


@cli.group()
def stack():
    """CLI sub-group for local Docker stack management."""


@stack.command()
def up():
    """Start the local Docker stack."""
    if not _docker_running():
        click.ClickException(
            click.style(
                "Docker is not running. Please start Docker and try again.", fg="red"
            )
        )

    subprocess.run(
        ["docker", "compose", "--file", str(DOCKER_COMPOSE_TEST), "up", "--detach"],
        check=True,
    )


@stack.command()
def down():
    """Stop the local Docker stack."""
    subprocess.run(
        ["docker", "compose", "--file", str(DOCKER_COMPOSE_TEST), "down"],
        check=True,
    )


@stack.command("create-database")
@click.option(
    "--add-data/--no-add-data",
    default=False,
    help="If data should be added to new database. [default: --no--add-data]",
)
def create_database(add_data):
    """Create the actual database in it."""
    from src.database_interface import (
        create_database,
        create_docker_postgresql_database_engine,
        add_test_data,
    )

    engine = create_docker_postgresql_database_engine()
    create_database(engine=engine)
    if add_data:
        add_test_data(engine=engine)
    else:
        click.echo("Empty Database has been created")


def _docker_running() -> bool:
    """Determine whether Docker is running."""
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


@stack.command()
def inspect_database():
    from src.database_interface import (
        create_docker_postgresql_database_engine,
    )
    from sqlalchemy import inspect

    engine = create_docker_postgresql_database_engine()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    for table_name in table_names:
        print(f"Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(
                f"  Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}"
            )


@stack.command()
def print_all_users():
    """Prints all users from the users table."""
    from sqlalchemy import inspect
    from sqlalchemy.orm import sessionmaker
    from src.database_interface import (
        create_docker_postgresql_database_engine,
    )
    from src.database_model import User

    engine = create_docker_postgresql_database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(User).all()

    inspector = inspect(engine)
    columns = inspector.get_columns("users")
    column_names = [col["name"] for col in columns]

    for user in users:
        user_data = {col: getattr(user, col) for col in column_names}
        print(user_data)  # print the dictionary of all fields and values.


if __name__ == "__main__":
    cli()
