import pytest

from api.scripts import ScriptManager


@pytest.mark.usefixtures("temp_paths")
def test_discover():
    mgr = ScriptManager()
    assert len(mgr._list) > 0

    from tests.dummy_scripts.script_dummy import dummy
    dummy1 = dummy
    dummy2 = mgr[dummy1.id]

    assert dummy1.exec(name='dummy1') == dummy2.exec(name='dummy1')
