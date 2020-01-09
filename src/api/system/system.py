from api.database import DBConn
from models import Base, User, UserHasRoles, Role
import logging

__all__ = ['SystemManager']


class SystemManager:
    def __init__(self):
        DBConn()

    def create_system_tables(self):
        DBConn.engine.execute(f'CREATE SCHEMA IF NOT EXISTS system')
        Base.metadata.create_all(bind=DBConn.engine)
        logging.info('Created system tables')

    def drop_schema(self, schema):
        DBConn.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')

    def drop_system_tables(self):
        self.drop_schema('system')
