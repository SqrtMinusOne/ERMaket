import pytest

from api.scripts import ScriptManager


@pytest.mark.usefixtures("temp_paths")
def test_discover():
    mgr = ScriptManager()
    assert len(mgr._list) > 0
