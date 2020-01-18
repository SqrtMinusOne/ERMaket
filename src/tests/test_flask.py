import pytest


def login(client, user):
    return client.post(
        '/auth/login', data={
            "login": user.login,
            "password": user.password
        }
    )


@pytest.mark.usefixtures("client", "test_db")
def test_login(test_db, client):
    assert not client.get('/auth/current').json['ok']
    assert not client.post('/auth/logout').json['ok']

    response = login(client, test_db.admin_user)
    assert response.json["ok"]

    response = client.get('/auth/current')
    assert response.json['user']['login'] == test_db.admin_user.login

    hierarchy = response.json['hierarchy']
    assert hierarchy
    assert len(next(iter(hierarchy['hierarchy']))['children']) > 0

    rights = response.json['rights']
    assert rights

    response = client.post('/auth/logout')
    assert response.json['ok']
    assert not client.get('/auth/current').json['ok']
    assert not client.post('/auth/logout').json['ok']


@pytest.mark.usefixtures("client", "test_db")
def test_get(client, test_db):
    schema = test_db.schema
    assert client.get('/tables/foo/bar').status_code == 404

    name = test_db.model.__table__.name
    table_url = f'/tables/table/{schema}/{name}'
    entry_url = f'/tables/entry/{schema}/{name}'
    assert client.get(table_url).status_code == 401
    assert client.get(entry_url).status_code == 401

    login(client, test_db.admin_user)

    response = client.get(table_url)
    assert len(response.json) > 0

    response = client.get(entry_url)
    assert response.json

    client.post('/auth/logout')
    login(client, test_db.normal_user)

    assert client.get(table_url).status_code == 403
    assert client.get(entry_url).status_code == 403
    client.post('/auth/logout')
