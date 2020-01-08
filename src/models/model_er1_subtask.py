import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Subtask']


class Er1Subtask(Base):
    __tablename__ = 'subtask'
    __table_args__ = {'schema': 'er1'}


    name = sa.Column(sa.String(256), primary_key=True, nullable=False, unique=True, autoincrement=False)

    task_id = sa.Column(sa.BigInteger(), sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'), primary_key=False, unique=False)

    task_contains = sa.orm.relationship('Er1Task', backref='contains', foreign_keys=[task_id])
