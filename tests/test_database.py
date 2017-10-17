from hypothesis import given, assume, strategies as st
import dpflask.db as database
import pandas as pd
import math
data = pd.read_json('https://data.iowa.gov/resource/wxib-fsgn.json?$limit=50000&$order=:id')
connection = database.connect_db()


@given(st.sampled_from(data.columns.values.tolist()), st.integers(min_value=0, max_value=(data.shape[0])))
def test_db(column, index):

    assume(column != 'primary_county_coordinates')
    cursor = connection.cursor()
    cursor.execute(f'SELECT "{column}" FROM dpflask WHERE "index"=?', (index,))
    test = cursor.fetchone()[0]
    actual = data.loc[index, column]
    if column == 'date':
        actual = str(actual)
    if isinstance(actual, float):
        assume(not math.isnan(actual))
    assert test == actual


columns = database.get_cols(connection)
parties = ['dem', 'lib', 'no_party', 'other', 'rep', None, st.text().example()]
activity = ['active', 'inactive', None, st.text().example()]


@given(st.sampled_from(parties), st.sampled_from(activity))
def test_filtercols(party, status):
    gen_cols = database.filter_columns(party, status)
    for col in gen_cols:
        assert col in columns
