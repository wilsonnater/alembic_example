# README

This is an example of using alembic to migrate a postgres database. It uses a dockerized postgres database so it is easy to spin up and down. (This is also
how I would test my database stuff)

# How to run the example migration

## Set-up environment

First build the environment using uv:
```
uv sync --frozen
```

The activate the environment:
```
source .venv/bin/activate
```

## Set-up database

In the main branch, start the postgres docker with:
```
python -m ci stack up
```
This requires docker to be running on your machine already.

The create a database and add data to it with:
```
python -m ci stack create-database --add-data
```

You can inspect that database to see all the tables with:
```
python -m ci stack inspect-database
```

You can also see all the users and user information with:
```
python -m ci stack print-all-users
```

## Perform Migration

Switch to the `nw/migration_example` branch:
```
git checkout nw/migration_example
```

Then run:
```
alembic upgrade head
```

The database is now migrated. This can be checked by running the inspect tables
and print all users commands.