import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Attachment']


class Er1Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'er1'}


    id = sa.Column(sa.BigInteger(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    contents = sa.Column(sa.Text(), primary_key=False, nullable=False, unique=False, autoincrement=False)

    task_id = sa.Column(sa.BigInteger(), sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'), primary_key=False, unique=False)

    task_is_attached = sa.orm.relationship('Er1Task', backref='is_attached', foreign_keys=[task_id])
