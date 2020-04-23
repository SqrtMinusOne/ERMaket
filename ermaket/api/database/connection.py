from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ermaket.api import Config

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
    def make_get_session(**kwargs):
        engine = DBConn.get_engine(**kwargs)
        Session = sessionmaker()
        Session.configure(bind=engine)

        @contextmanager
        def get_session(**session_kwargs):
            session = Session(**session_kwargs)
            yield session
            session.close()

        return get_session

    @staticmethod
    @contextmanager
    def get_session(**kwargs):
        """
        Get automatically closing sessions

        Usage:
        ```
        with DBConn.get_session() as session:
            # do stuff
        ```
        """
        session = DBConn.Session(**kwargs)
        yield session
        session.close()

    @staticmethod
    @contextmanager
    def ensure_session(session, **kwargs):
        """
        If session is None, make a new one
        """
        if session is None:
            session = DBConn.Session(**kwargs)
            yield session
            session.close()
        else:
            yield session

    @staticmethod
    def get_engine(user=None, password=None, **kwargs):
        """Initialize SQLAlchemy engine from configuration parameters

        :param **kwargs: to sqlalchemy.create_engine
        """
        config = Config()
        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user or config.Database['user'], password or
            config.Database['password'], config.Database['host'],
            config.Database['port'], config.Database['database']
        )
        return create_engine(url, **kwargs)
