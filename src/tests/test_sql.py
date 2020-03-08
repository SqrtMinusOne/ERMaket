import pytest

from api.database import DBConn, DatabaseUserManager
from api.queries import SqlExecutor


@pytest.mark.usefixtures('test_db', 'config')
def test_init(test_db, config):
    u1 = config.Users['readonly']['user']
    u2 = config.Users['sql']['user']
    users = DatabaseUserManager()
    users.drop_user(u1)
    users.drop_user(u2)

    SqlExecutor()
    with DBConn.get_session() as db:
        user_select = db.execute(
            f"SELECT 1 from pg_roles WHERE rolname='{u1}'"
        ).first()
        assert user_select
        user_select = db.execute(
            f"SELECT 1 from pg_roles WHERE rolname='{u2}'"
        ).first()
        assert user_select


@pytest.mark.usefixtures('test_db')
def test_execute(test_db):
    schema, table = test_db.schema, test_db.entry.tableName
    executor = SqlExecutor()

    query = f'SELECT * FROM {schema}.{table}'
    for user in (None, 'readonly', 'sql'):
        res, keys = executor.execute(query, user=user)
        assert len(res) > 0 and len(keys) > 0
