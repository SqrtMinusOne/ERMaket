import sqlalchemy as sa

from .base import Base

__all__ = ['Er1User']


class Er1User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'er1'}


    name = sa.Column(sa.String(256), primary_key=True, nullable=False, unique=True, autoincrement=False)

