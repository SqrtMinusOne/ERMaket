from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from api import Config
from contextlib import contextmanager


__all__ = ['DBConn']


class DBConn:
    """
    A facade for creating sessions. Has to be instantiated before the first
    use, after that - DBConn.Session() to create session.

    Engine is created with config.json

    """
    engine = None
    Session = None
    scoped_session
    Base = None

    def __init__(self, **kwargs):
        DBConn.engine = DBConn.get_engine(**kwargs)
        DBConn.Session = sessionmaker()
        DBConn.Session.configure(bind=self.engine)
        DBConn.scoped_session = scoped_session(DBConn.Session)

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
    @contextmanager
    def ensure_session(session):
        """
        If session is None, make a new one
        """
        if session is None:
            session = DBConn.Session()
            yield session
            session.close()
        else:
            yield session

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
