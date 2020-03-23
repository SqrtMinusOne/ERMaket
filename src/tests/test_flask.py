import json

import pytest

from api.database import DBConn


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


def print_roles(test_db):
    from api.database import DBConn
    normal, admin = test_db.normal_user.user, test_db.admin_user.user
    with DBConn.get_session() as db:
        db.add(normal)
        db.add(admin)
        print(f'Normal roles: {normal.role_names}')
        print(f'Admin roles: {admin.role_names}')


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
    assert response.status_code == 200
    assert len(response.json) > 0

    response = client.get(entry_url)
    assert response.status_code == 200
    assert response.json

    client.post('/auth/logout')
    login(client, test_db.normal_user)

    # assert client.get(table_url).status_code == 403
    # assert client.get(entry_url).status_code == 403
    client.post('/auth/logout')


@pytest.mark.usefixtures("client", "test_db")
def test_transaction(client, test_db):
    model = test_db.model
    entry = test_db.entry

    with DBConn.get_session() as db:
        item = db.query(model).first()
        data = model.__marshmallow__().dump(item)
        key = data[entry.pk.rowName]

        transaction = {entry.id: {'delete': {key: True}}}
    login(client, test_db.admin_user)
    response = client.post(
        '/transaction/execute',
        data=json.dumps({'transaction': transaction}),
        content_type='application/json'
    )

    assert response.status_code == 200


@pytest.mark.usefixtures("client", "test_db")
def test_sql(client, test_db):
    schema, table = test_db.schema, test_db.entry.tableName

    query = f'SELECT * FROM {schema}.{table}'
    login(client, test_db.admin_user)

    response = client.post(
        '/sql/execute',
        data=json.dumps({'query': query}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert len(response.json["result"][0]) == len(response.json["keys"])


@pytest.mark.usefixtures("client", "test_db")
def test_call_script(client, test_db):
    login(client, test_db.admin_user)
    response = client.post(
        "/scripts/execute/1",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['business_logic']['done'] == 'step_1'

    response = client.post(
        "/scripts/execute/1",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['business_logic']['done'] == 'step_2'

    response = client.post(
        "/scripts/execute/1",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['business_logic']['done'] == 'step_1'
