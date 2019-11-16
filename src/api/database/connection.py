from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import Config
from contextlib import contextmanager
from models.base import Base


__all__ = ['DBConn']


class DBConn:
    """
    A facade for creating sessions. Has to be instantiated before the first
    use, after that - DBConn.Session() to create session.

    Engine is created with config.json

    """
    engine = None
    Session = None
    Base = None

    def __init__(self, **kwargs):
        DBConn.engine = DBConn.get_engine(**kwargs)
        DBConn.Session = sessionmaker()
        DBConn.Session.configure(bind=self.engine)
        DBConn.Base = Base

    @classmethod
    def reset(cls):
        cls.engine = cls.Session = None

    @staticmethod
    @contextmanager
    def get_session():
        """
        Get automatically closing sessions

        Usage:
        ```
        with DBConn.get_session() as session:
            # do stuff
        ```
        """
        session = DBConn.Session()
        yield session
        session.close()

    @staticmethod
    def get_engine(**kwargs):
        """Initialize SQLAlchemy engine from configuration parameters

        :param **kwargs: to sqlalchemy.create_engine
        """
        config = Config()
        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            config.Database['user'],
            config.Database['password'],
            config.Database['host'],
            config.Database['port'],
            config.Database['database']
        )
        return create_engine(url, **kwargs)
