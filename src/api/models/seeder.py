from api.database import DBConn

from .models import Models

__all__ = ['Seeder']


class Seeder:
    """
    Class for initializing or clearing the database
    """
    def __init__(self, models: Models):
        self._models = models

    def create_models(self):
        """Creates all imported models if they do not exist
        """
        for schema in self._models.schemas.keys():
            DBConn.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')
        self._models.Base.metadata.create_all(bind=DBConn.engine)

    def drop_models(self, schema=None):
        """Drops models

        :param schema: if given, drops only ones in the given schema
        """
        if schema is not None:
            DBConn.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')
            return
        for schema in self._models.schemas.keys():
            DBConn.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')
