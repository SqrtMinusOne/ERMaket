import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Comment']


class Er1Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'schema': 'er1'}


    id = sa.Column(sa.BigInteger(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    text = sa.Column(sa.Text(), primary_key=False, nullable=False, unique=False, autoincrement=False)

    user_name = sa.Column(sa.String(256), sa.ForeignKey('er1.user.name', ondelete='cascade', onupdate='cascade'), primary_key=False, unique=False)
    task_id = sa.Column(sa.BigInteger(), sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'), primary_key=False, unique=False)

    user_is_authored_by = sa.orm.relationship('Er1User', backref='is_authored_by', foreign_keys=[user_name])

    task_is_written_to = sa.orm.relationship('Er1Task', backref='is_written_to', foreign_keys=[task_id])
