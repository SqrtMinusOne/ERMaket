import pytest

from api.system import UserManager


@pytest.mark.usefixtures('empty_db')
def test_create(test_db):
    manager = UserManager()
    assert manager.check_user('manager', 'password') is None
    manager.add_user('manager', 'password')
    assert manager.check_user('manager', 'password')
    manager.check_user('manager', 'password1') is None
    manager.check_user('manager1', 'password') is None
