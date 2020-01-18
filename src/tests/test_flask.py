import pytest


@pytest.mark.usefixtures("client", "test_db")
def test_login(test_db, client):
    assert not client.get('/auth/current').json['ok']
    assert not client.post('/auth/logout').json['ok']

    response = client.post(
        '/auth/login',
        data={
            "login": test_db.login,
            "password": test_db.password
        }
    )

    assert response.json["ok"]

    response = client.get('/auth/current')
    assert response.json['login'] == test_db.login

    hierarchy = response.json['user_hierarchy']
    assert hierarchy
    assert len(next(iter(hierarchy['hierarchy']))['children']) > 0

    response = client.post('/auth/logout')
    assert response.json['ok']
    assert not client.get('/auth/current').json['ok']
    assert not client.post('/auth/logout').json['ok']
