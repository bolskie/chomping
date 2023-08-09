#!/usr/bin/env python

"""upload_contributor.py: upload recipe data from memory to database file"""

__author__ = "bolskie"
__copyright__ = "copyright 2023, Jack Briskie"

import pathlib
import sqlite3
from typing import Union


def match_contributor(db_path: Union[str, pathlib.Path], contributor_value: str) -> Union[int, None]:
    """look up primary key id of contributor table matching input name.

    :param db_path: path to database file containing contributor table
    :param contributor_value: string of contributor name from recipe input file
    :returns: id primary key from contributor table
    """
    # read SQL query from file
    sql_file = open(pathlib.Path(__file__).parent.resolve() / "match_contributor.sql")
    sql_query = sql_file.read()
    sql_file.close()

    # populate SQL string with value from function input
    format_sql_query = sql_query.format(contributor_value)

    # query database to return primary key id of matching record, return None if no match
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        contributor_id = list(cur.execute(format_sql_query))[0][0]
    except IndexError:
        contributor_id = None
    finally:
        conn.close()
    return contributor_id


def upload_contributor(db_path: Union[str, pathlib.Path], contributor_value: str) -> int:
    """write input contributor name to database.

    :param db_path: path to database file containing contributor table
    :param contributor_value: string of contributor name from recipe input file
    :returns: id primary key from contributor table, whether existing or newly written data
    """
    # read SQL query from file
    sql_file = open(pathlib.Path(__file__).parent.resolve() / "insert_contributor.sql")
    sql_statement = sql_file.read()
    sql_file.close()

    # search database for existing contributor record
    contributor_match = match_contributor(db_path=db_path, contributor_value=contributor_value)
    if contributor_match:
        # do not write data if already exists in database
        pass
    else:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute(sql_statement, contributor_value)
        conn.commit()
        conn.close()

        # search database again to confirm data write
        contributor_match = match_contributor(db_path=db_path, contributor_value=contributor_value)

    return contributor_match
