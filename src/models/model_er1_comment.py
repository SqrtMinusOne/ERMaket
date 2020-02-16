# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa

from .base import Base

__all__ = ['Er1Comment']


class Er1Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = ({'schema': 'er1'})

    id = sa.Column(
        sa.BigInteger(),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    text = sa.Column(
        sa.Text(),
        nullable=False,
    )

    user_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.user.name', ondelete='cascade', onupdate='cascade'),
        nullable=True,
    )
    task_id = sa.Column(
        sa.BigInteger(),
        sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'),
        nullable=True,
    )

    is_authored_by_user = sa.orm.relationship(
        'Er1User',
        back_populates='comment_is_authored_by',
        foreign_keys=[user_name]
    )
    is_written_to_task = sa.orm.relationship(
        'Er1Task',
        back_populates='comment_is_written_to',
        foreign_keys=[task_id]
    )
