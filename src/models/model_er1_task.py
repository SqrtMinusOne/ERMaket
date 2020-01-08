import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Task']


class Er1Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'er1'}


    id = sa.Column(sa.BigInteger(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = sa.Column(sa.String(256), primary_key=False, nullable=False, unique=False, autoincrement=False)
    due_date = sa.Column(sa.DateTime(), primary_key=False, nullable=False, unique=False, autoincrement=False)
    description = sa.Column(sa.Text(), primary_key=False, nullable=False, unique=False, autoincrement=False)

    list_id = sa.Column(sa.BigInteger(), sa.ForeignKey('er1.list.id', ondelete='cascade', onupdate='cascade'), primary_key=False, unique=False)

    list_belongs_to = sa.orm.relationship('Er1List', backref='belongs_to', foreign_keys=[list_id])
