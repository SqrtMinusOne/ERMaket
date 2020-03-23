import pytest

from api.scripts import ScriptManager, Context

CHAIN_ID = 1


@pytest.mark.usefixtures("temp_paths")
def test_discover():
    mgr = ScriptManager()
    assert len(mgr._list) > 0

    from tests.dummy_scripts.script_dummy import dummy
    dummy1 = dummy
    dummy2 = mgr[dummy1.id]

    assert dummy1.exec(name='dummy1') == dummy2.exec(name='dummy1')


@pytest.mark.usefixtures("temp_paths", "dummy_session")
def test_chain(dummy_session):
    mgr = ScriptManager()
    mgr.set_session(dummy_session)
    ctx1 = Context()
    res1 = mgr.execute(CHAIN_ID, ctx1)
    assert res1.abort is None
    assert ctx1.exec_data['data'] is not None

    ctx2 = Context()
    res2 = mgr.execute(CHAIN_ID, ctx2)
    assert res2.abort is None
    assert ctx1.exec_data['data'] == ctx2.exec_data['data']
