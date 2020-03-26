import json

import pytest

from api.database import DBConn
from api.scripts import ScriptManager
from api.system.hierarchy import Activation, Trigger, Triggers

CHAIN_ID = 1
TEAPOT_ID = 2
ADD_ID = 3
ADD2_ID = 4


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

    profile_forms = response.json['profile_forms']
    assert len(profile_forms) > 0

    response = client.post('/auth/logout')
    assert response.json['ok']
    assert not client.get('/auth/current').json['ok']
    assert not client.post('/auth/logout').json['ok']


@pytest.mark.usefixtures("client", "test_db")
def test_password(test_db, client):
    assert login(client, test_db.admin_user).json["ok"]

    assert not client.post(
        '/auth/password',
        data={
            "old_pass": "Surely wrong password, noone would ever set this",
            "new_pass": "1234567890"
        }
    ).json['ok']

    client.post('/auth/logout')
    assert login(client, test_db.admin_user).json["ok"]

    assert client.post(
        '/auth/password',
        data={
            "old_pass": test_db.admin_user.password,
            "new_pass": "1234567890"
        }
    ).json["ok"]
    client.post('/auth/logout')
    assert not login(client, test_db.admin_user).json["ok"]
    assert client.post(
        '/auth/login',
        data={
            "login": test_db.admin_user.login,
            "password": "1234567890"
        }
    ).json["ok"]
    assert client.post(
        '/auth/password',
        data={
            "old_pass": "1234567890",
            "new_pass": test_db.admin_user.password
        }
    ).json["ok"]
    client.post('/auth/logout')


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
        f"/scripts/execute/{CHAIN_ID}",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['businessLogic']['done'] == 'step_1'

    response = client.post(
        f"/scripts/execute/{CHAIN_ID}",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['businessLogic']['done'] == 'step_2'

    response = client.post(
        f"/scripts/execute/{CHAIN_ID}",
        data=json.dumps({'activation': 'call'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['businessLogic']['done'] == 'step_1'


@pytest.mark.usefixtures("client", "test_db")
def test_abort_request(client, test_db):
    test_db.entry.triggerList = Triggers([Trigger(Activation.READ, TEAPOT_ID)])
    login(client, test_db.admin_user)

    schema, name = test_db.entry.schema, test_db.entry.tableName
    table_url = f'/tables/table/{schema}/{name}'
    entry_url = f'/tables/entry/{schema}/{name}'
    assert client.get(table_url).status_code == 418
    assert client.get(entry_url).status_code == 418

    mgr = ScriptManager()
    mgr.global_triggers.append(Trigger(Activation.TRANSACTION, TEAPOT_ID))
    model = test_db.model
    entry = test_db.entry

    with DBConn.get_session() as db:
        item = db.query(model).first()
        data = model.__marshmallow__().dump(item)
        key = data[entry.pk.rowName]

        transaction = {entry.id: {'delete': {key: True}}}
    response = client.post(
        '/transaction/execute',
        data=json.dumps({'transaction': transaction}),
        content_type='application/json'
    )
    assert response.status_code == 418
    client.post('/auth/logout')

    mgr.global_triggers.append(Trigger(Activation.LOGIN, TEAPOT_ID))
    response = client.post(
        '/auth/login',
        data={
            "login": test_db.admin_user.login,
            "password": test_db.admin_user.password
        }
    )
    assert response.status_code == 418
    mgr.global_triggers = Triggers([])


@pytest.mark.usefixtures("client", "test_db")
def test_add_info(client, test_db):
    mgr = ScriptManager()
    mgr.global_triggers.append(Trigger(Activation.LOGIN, ADD_ID))
    response = client.post(
        '/auth/login',
        data={
            "login": test_db.admin_user.login,
            "password": test_db.admin_user.password
        }
    )
    assert response.status_code == 200
    assert response.json['businessLogic']['data'] == "EXAMPLE_DATA"
    client.post('/auth/logout')

    mgr.global_triggers.append(Trigger(Activation.LOGIN, ADD2_ID))
    response = client.post(
        '/auth/login',
        data={
            "login": test_db.admin_user.login,
            "password": test_db.admin_user.password
        }
    )
    assert response.status_code == 200
    assert response.json['businessLogic']['data'] == "EXAMPLE_DATA"
    assert response.json['businessLogic']['data2'] == "EXAMPLE_DATA2"
    mgr.global_triggers = Triggers([])
