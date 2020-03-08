import logging

from api import Config
from api.database import DBConn
from api.models import Models

__all__ = ['SqlExecutor']


class SqlExecutor:
    def __init__(self):
        self._config = Config()
        self._models = Models()
        self._create_readonly_user()

    def _create_readonly_user(self):
        # TODO It may be a temporary solution
        with DBConn.get_session() as db:
            config = {
                **self._config.Database,
                **self._config.Users['readonly']
            }
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
                logging.info(f'Created read-only user "{config["user"]}"')

            for schema in self._models.schema_names:
                db.execute(
                    f'GRANT USAGE ON SCHEMA {schema} TO {config["user"]}'
                )
                db.execute(
                    f'GRANT SELECT ON ALL TABLES IN SCHEMA {schema} '
                    f'TO {config["user"]}'
                )
            logging.info(
                f'Updated read-only user rights for'
                f' {len(self._models.schema_names)} schemas'
            )
            db.commit()
