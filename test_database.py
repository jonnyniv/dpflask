from hypothesis import given, assume, strategies as st
import dpflask.db as database
import pandas as pd
import math
data = pd.read_csv('iowa.csv')


@given(st.sampled_from(data.columns.values.tolist()), st.integers(min_value=0, max_value=(data.shape[0])))
def test_db(column, index):
    cursor = database.connection.cursor()
    cursor.execute(f'SELECT "{column}" FROM dpflask WHERE "index"=?', (index,))
    test = cursor.fetchone()[0]
    actual = data.loc[index, column]
    if isinstance(actual, float):
        assume(not math.isnan(actual))
    assert test == actual
