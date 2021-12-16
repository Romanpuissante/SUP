from sqlalchemy import Column, Table, Integer
from conf.db import metadata


def create_table(name, columns: tuple):
    return Table(
        name,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        *columns,
    )

