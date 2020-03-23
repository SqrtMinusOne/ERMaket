from sqlalchemy.exc import ResourceClosedError

from api import Config
from api.database import DatabaseUserManager, DBConn
from api.models import Models
from utils import Singleton

__all__ = ['SqlExecutor']


class SqlExecutor(metaclass=Singleton):
    def __init__(self):
        self._config = Config()
        self._models = Models()
        self._users = DatabaseUserManager()

        self._get_session = {}

        self._create_users()

    def _create_users(self):
        self._users.create_user(self._config.Users['readonly'], ('SELECT', ))
        self._users.create_user(
            self._config.Users['sql'],
            ('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE')
        )
        self._get_session = {
            'readonly':
                DBConn.make_get_session(
                    user=self._config.Users['readonly']['user'],
                    password=self._config.Users['readonly']['password']
                ),
            'sql':
                DBConn.make_get_session(
                    user=self._config.Users['sql']['user'],
                    password=self._config.Users['sql']['password']
                ),
        }

    def execute(self, query, user=None):
        with self._session(user)() as db:
            result_proxy = db.execute(query)
            try:
                rows = result_proxy.fetchall()
                keys = result_proxy.keys()
                db.commit()
                return self._serialize(rows), keys
            except ResourceClosedError:
                db.commit()
                return None, None

    def _serialize(self, rows):
        return [list(row) for row in rows]

    def _session(self, user):
        return self._get_session.get(user, DBConn.get_session)
