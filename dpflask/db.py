import os
import sqlite3
from typing import List

import pandas as pd


def connect_db() -> sqlite3.Connection:
    return sqlite3.connect(os.path.join(os.path.dirname(__file__), 'dpflask.db'))


def get_cols(connection: sqlite3.Connection) -> List[str]:
    colcurs = connection.cursor()
    colcurs.execute("SELECT * FROM dpflask")
    columns = next(zip(*colcurs.description))
    return columns


def filter_columns(party: str, status: str) -> List[str]:
    new_cols = ['county', 'date']
    parties = ['dem', 'lib', 'no_party', 'other', 'rep']
    activity = ['active', 'inactive']
    ps = []
    if party and party in parties:
        ps.append(party)
    else:
        ps = parties
    if status and status in activity:
        ps = ['_'.join((p, status)) for p in ps]
    else:
        ps = ['_'.join((p, s)) for p in ps for s in activity]
    return new_cols + ps


def get_args(args):
    county = args.get('county', '')
    party = args.get('party', '')
    status = args.get('status', '')
    month = args.get('month', '')
    limit = args.get('limit', 100)
    return county, party, status, month, limit


def get_voters_where(args, connection: sqlite3.Connection) -> list:
    county, party, status, month, limit = get_args(args)
    new_columns = filter_columns(party, status)
    base_query = "SELECT {} FROM dpflask".format(', '.join(new_columns))
    cursor = connection.cursor()
    params = []
    for param, name in zip((county, month), ('county', 'month')):
        if param:
            params.append(param)
            if 'WHERE' in base_query:
                base_query += f' AND {name}=?'
            else:
                base_query += f' WHERE {name}=?'

    if limit is not None:
        base_query += " LIMIT ?"
        params.append(limit)

    cursor.execute(base_query, params)
    connection.commit()
    df = pd.DataFrame(cursor.fetchall(), columns=new_columns)
    output = [row.to_dict() for _, row in df.iterrows()]

    return output
