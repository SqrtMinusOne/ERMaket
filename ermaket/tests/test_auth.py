import pytest

from ermaket.api.system import UserManager


@pytest.mark.usefixtures('empty_db')
def test_create(test_db):
    manager = UserManager()
    assert manager.check_user('manager', 'password') is None
    manager.add_user('manager', 'password')
    assert manager.check_user('manager', 'password')
    manager.check_user('manager', 'password1') is None
    manager.check_user('manager1', 'password') is None


@pytest.mark.usefixtures('empty_db')
def test_register(test_db):
    manager = UserManager()
    token_hash = manager.add_register_token('test1')
    for i in range(10):
        assert manager.register_user(token_hash, f'user{i}', 'pwd') is not None

    token_hash = manager.add_register_token('test2', uses=1)
    assert manager.register_user(token_hash, 'user-11', 'pwd') is not None
    assert manager.register_user(token_hash, 'user-12', 'pwd') is None


@pytest.mark.usefixtures('empty_db')
def test_reset_password(test_db):
    manager = UserManager()
    manager.add_user('user-13', 'password')
    token_hash = manager.add_reset_password_token('test3', 'user-13', uses=1)
    assert manager.reset_password(token_hash, 'user-13', '12345')
    assert manager.check_user('user-13', '12345')
    assert not manager.check_user('user-13', 'password')

    token_hash = manager.add_register_token('test4')
    assert not manager.reset_password(token_hash, 'user-13', '1234567')

    token_hash = manager.add_reset_password_token('test3', 'user-14', uses=1)
    assert not manager.reset_password(token_hash, 'user-13', '1234567')
