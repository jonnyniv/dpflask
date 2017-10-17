from hypothesis import given, assume, strategies as st
import dpflask.db as database
import pandas as pd
import math
data = pd.read_json('https://data.iowa.gov/resource/wxib-fsgn.json?$limit=50000&$order=:id')


@given(st.sampled_from(data.columns.values.tolist()), st.integers(min_value=0, max_value=(data.shape[0])))
def test_db(column, index):
    assume(column != 'primary_county_coordinates')
    cursor = database.connection.cursor()
    cursor.execute(f'SELECT "{column}" FROM dpflask WHERE "index"=?', (index,))
    test = cursor.fetchone()[0]
    actual = data.loc[index, column]
    if column == 'date':
        actual = str(actual)
    if isinstance(actual, float):
        assume(not math.isnan(actual))
    assert test == actual
