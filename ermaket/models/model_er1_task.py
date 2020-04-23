# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa

from ermaket.models.base import Base

__all__ = ['Er1Task']


class Er1Task(Base):
    __tablename__ = 'task'
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
    due_date = sa.Column(
        sa.DateTime(),
        nullable=False,
    )
    description = sa.Column(
        sa.Text(),
        nullable=False,
    )

    list_id = sa.Column(
        sa.BigInteger(),
        sa.ForeignKey(
            'er1.list.id',
            ondelete='cascade',
            onupdate='cascade',
            deferrable=True,
            initially="DEFERRED"
        ),
        nullable=False,
    )

    comment_is_written_to = sa.orm.relationship(
        'Er1Comment', back_populates='is_written_to_task'
    )

    belongs_to_list = sa.orm.relationship(
        'Er1List', back_populates='task_belongs_to', foreign_keys=[list_id]
    )
    attachment_is_attached = sa.orm.relationship(
        'Er1Attachment', back_populates='is_attached_task'
    )

    subtask_contains = sa.orm.relationship(
        'Er1Subtask', back_populates='contains_task'
    )

    is_assigned_to_user = sa.orm.relationship(
        'Er1User',
        secondary='er1.user_is_assigned_to_task',
        back_populates='is_assigned_to_task'
    )
