# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa

from ermaket.models.base import Base

__all__ = ['Er1Item']


class Er1Item(Base):
    __tablename__ = 'item'
    __table_args__ = ({'schema': 'er1'})

    id = sa.Column(
        sa.BigInteger(),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    name = sa.Column(
        sa.String(256),
        nullable=False,
    )
    status = sa.Column(
        sa.Enum('Complete', 'Not complete', name='status'),
        nullable=False,
    )

    subtask_name = sa.Column(
        sa.String(256),
        sa.ForeignKey(
            'er1.subtask.name',
            ondelete='cascade',
            onupdate='cascade',
            deferrable=True,
            initially="DEFERRED"
        ),
        nullable=False,
    )

    contains_subtask = sa.orm.relationship(
        'Er1Subtask',
        back_populates='item_contains',
        foreign_keys=[subtask_name]
    )
