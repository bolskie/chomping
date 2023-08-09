#!/usr/bin/env python

"""upload_recipe_data.py: upload recipe data from memory to database file"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import sqlite3
from typing import Union, Literal
from collections.abc import Iterable


def read_sql_file(
    file_prefix: Literal["match", "insert"],
    db_table: Literal["contributor", "dish", "ingredient", "method", "recipe"],
) -> str:
    """read SQL script from file and return as string.

    :param file_prefix: prefix of SQL query as string
    :param db_table: name of table to search input as string
    :returns: SQL script from file as string
    """
    # generate file path from input selections
    file_name = "".join((file_prefix, "_", db_table, ".sql"))
    main_path = pathlib.Path(__file__).parent.resolve()
    sql_path = main_path / file_name

    # read SQL query from file
    try:
        sql_file = open(sql_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL query not found in {sql_path}")
    sql_query = sql_file.read()
    sql_file.close()
    return sql_query


def match_data(
    db_path: Union[str, pathlib.Path],
    db_table: Literal["contributor", "dish", "ingredient", "method", "recipe"],
    lookup_values: Union[str, tuple],
) -> Union[int, None]:
    """look up primary key id of from selected table matching input data.

    :param db_path: path to database file to search
    :param db_table: name of table to search input as string
    :param lookup_values: data to match and look up primary key
    :returns: id primary key from selected table matching input data
    """
    # read SQL from file
    sql_query = read_sql_file(file_prefix="match", db_table=db_table)

    # populate SQL string with value(s) from function input
    if isinstance(lookup_values, Iterable):
        format_sql_query = sql_query.format(*lookup_values)
    else:
        format_sql_query = sql_query.format(lookup_values)

    # query database to return primary key id of matching record, return None if no match
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        match_id = list(cur.execute(format_sql_query))[0][0]
    except IndexError:
        match_id = None
    finally:
        conn.close()
    return match_id


def upload_data(
    db_path: Union[str, pathlib.Path],
    db_table: Literal["contributor", "dish", "ingredient", "method", "recipe"],
    upload_values: Union[str, tuple],
) -> int:
    """write input data to database at selected table.

    :param db_path: path to database file to write data to
    :param db_table: name of table to write to
    :param upload_values: data to write to database file
    :returns: id primary key from contributor table, whether existing or newly written data
    """
    # read SQL from file
    sql_statement = read_sql_file(file_prefix="insert", db_table=db_table)

    # search database for existing record
    data_match = match_data(
        db_path=db_path, db_table=db_table, lookup_values=upload_values
    )
    if data_match:
        # do not write data if already exists in database
        pass
    else:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute(sql_statement, upload_values)
        conn.commit()
        conn.close()

        # search database again to confirm data write
        data_match = match_data(
            db_path=db_path, db_table=db_table, lookup_values=upload_values
        )

    return data_match
