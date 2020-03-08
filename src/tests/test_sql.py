import pytest

from api.database import DBConn
from api.queries import SqlExecutor


@pytest.mark.usefixtures('test_db', 'config')
def test_create_readonly_user(test_db, config):
    executor = SqlExecutor()
    user = config.Users['readonly']
    with DBConn.get_session() as db:
        try:
            db.execute(f'DROP OWNED BY {user["user"]}')
            db.execute(f'DROP USER {user["user"]}')
        except Exception:
            pass
    executor._create_readonly_user()
    with DBConn.get_session() as db:
        user_select = db.execute(
            f"SELECT 1 from pg_roles WHERE rolname='{user['user']}'"
        ).first()
        assert user_select
