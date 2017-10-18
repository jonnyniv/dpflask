from hypothesis import strategies as st, given
import dpflask


app = dpflask.app.test_client()
app.testing = True


def test_gvw_endpoint_ok():
    """Test that the basic endpoint is available"""
    req = app.get('/get_voters_where')
    assert req.status == '200 OK'


@given(st.text())
def test_endpoint_cab(v):
    """All endpoints should be safe and not cause errors"""
    req = app.get('/' + v)
    assert not req.status.startswith('5')


@given(st.text())
def test_gvw_endpoint_graceful(v):
    """Get voters where should never cause an internal server error"""
    req = app.get('/get_voters_where?'+v)
    assert not req.status.startswith('5')


valid_vars = ['county', 'party', 'status', 'month', 'limit']
valid_vars_strat = st.dictionaries(st.one_of(st.sampled_from(valid_vars), st.text()), st.text(), max_size=5)


@given(valid_vars_strat)
def test_valid_ep(req_dict: dict):
    req_str = '?'
    for k, v in req_dict.items():
        req_str += f'{k}={v}&'

    req = app.get('/get_voters_where' + req_str)
    assert not req.status.startswith('5')
