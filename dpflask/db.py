import os
import sqlite3
from typing import List

import pandas as pd

connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'dpflask.db'))


def create_db():
    df = pd.read_csv('../iowa.csv')
    months = df['Date']
    df['Month'] = [row[:2] for _, row in months.iteritems()]
    df.to_sql('dpflask', connection, if_exists='replace')


# create_db()


def get_cols():
    colcurs = connection.cursor()
    colcurs.execute("SELECT * FROM dpflask")
    columns = next(zip(*colcurs.description))
    return columns

columns = get_cols()
party_status = [a for a in [[x.strip() for x in col.split('-')] for col in columns] if len(a) > 1]
party_dict = {}
status_dict = {}
all_parts = set()
for ps in party_status:
    party_stat_str = {ps[0] + ' - ' + ps[1]}
    par = party_dict.get(ps[0], set())
    stat = status_dict.get(ps[1], set())
    par |= party_stat_str
    stat |= party_stat_str
    all_parts |= party_stat_str
    party_dict[ps[0]] = par
    status_dict[ps[1]] = stat


def list_ps(party: str = '', status: str = '') -> List[str]:
    if party and status:
        return [f'{party} - {status}']
    elif party:
        return [a for a in party_dict[party]]
    elif status:
        return [a for a in status_dict[status]]
    else:
        return list(all_parts)


def get_voters_where(county: str = '', month: str = '', party: str = '', status: str = '', limit: int = None) -> list:
    base_query = "SELECT * FROM dpflask"
    cursor = connection.cursor()
    params = []
    if month: month = month.zfill(2)
    for param, name in zip((county, month), ('County', 'Month')):
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
    df = pd.DataFrame(cursor.fetchall(), columns=columns).set_index('index')
    party_stat = list_ps(party, status)
    if month:
        df = df.loc[df['Date'].str.startswith(month)]
    if party_stat:
        df = pd.merge(df[party_stat], df[['Date', 'County', 'Grand Total']], left_index=True, right_index=True)
    output = [row.to_dict() for _, row in df.iterrows()]

    return output
