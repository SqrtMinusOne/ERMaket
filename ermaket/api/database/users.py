import logging

from boltons.setutils import IndexedSet

from ermaket.api import Config
from ermaket.api.database import DBConn
from ermaket.api.models import Models
from ermaket.utils import Singleton

__all__ = ['DatabaseUserManager']


class DatabaseUserManager(metaclass=Singleton):
    def __init__(self):
        self._config = Config()
        self._models = Models()

    def drop_user(self, name):
        with DBConn.get_session() as db:
            try:
                db.execute(f'DROP OWNED BY {name}')
                db.execute(f'DROP USER {name}')
                return True
            except Exception:
                return False

    def create_user(self, config, rights):
        with DBConn.get_session() as db:
            config = {**self._config.Database, **config}
            self._try_create_user(config, db)
            if isinstance(rights, list) or isinstance(rights, tuple):
                for schema in self._models.schema_names:
                    self._grant_rights_on_schema(config, db, schema, rights)
            else:
                for schema, rights_ in rights.items():
                    self._grant_rights_on_schema(config, db, schema, rights_)
            db.commit()

    def _try_create_user(self, config, db):
        user_select = db.execute(
            f"SELECT 1 from pg_roles WHERE rolname='{config['user']}'"
        ).first()
        if not user_select:
            db.execute(
                f'CREATE USER {config["user"]}'
                f" WITH PASSWORD '{config['password']}'"
            )
            db.execute(
                f'GRANT CONNECT ON DATABASE {config["database"]} '
                f'to {config["user"]}'
            )
            logging.info(f'Created  user "{config["user"]}"')

    def _grant_rights_on_schema(self, config, db, schema, rights):
        schema_rights = self._schema_rights(rights)
        table_rights = self._table_rights(rights)

        db.execute(
            f'GRANT {", ".join(schema_rights)} '
            f'ON SCHEMA {schema} TO {config["user"]}'
        )
        db.execute(
            f'GRANT {", ".join(table_rights)} ON ALL TABLES '
            f'IN SCHEMA {schema} TO {config["user"]}'
        )
        logging.info(
            f'Granted {", ".join(rights)} on {schema} '
            f'to {config["user"]}'
        )

    def _schema_rights(self, rights):
        schema_rights = ['USAGE']
        if 'CREATE' in rights:
            schema_rights.append('CREATE')
        return schema_rights

    def _table_rights(self, rights):
        vals = IndexedSet(
            [
                'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE',
                'REFERENCES', 'TRIGGER'
            ]
        )
        return vals.intersection(set(rights))
