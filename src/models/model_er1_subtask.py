# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Subtask']


class Er1Subtask(Base):
    __tablename__ = 'subtask'
    __table_args__ = ({'schema': 'er1'})

    name = sa.Column(
        sa.String(256),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    task_id = sa.Column(
        sa.BigInteger(),
        sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'),
        nullable=True,
    )

    contains_task = sa.orm.relationship(
        'Er1Task', back_populates='subtask_contains', foreign_keys=[task_id]
    )
    item_contains = sa.orm.relationship(
        'Er1Item', back_populates='contains_subtask'
    )
