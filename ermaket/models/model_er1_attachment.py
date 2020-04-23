# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa

from ermaket.models.base import Base

__all__ = ['Er1Attachment']


class Er1Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = ({'schema': 'er1'})

    id = sa.Column(
        sa.BigInteger(),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    contents = sa.Column(
        sa.Text(),
        nullable=False,
    )

    task_id = sa.Column(
        sa.BigInteger(),
        sa.ForeignKey(
            'er1.task.id',
            ondelete='cascade',
            onupdate='cascade',
            deferrable=True,
            initially="DEFERRED"
        ),
        nullable=False,
    )

    is_attached_task = sa.orm.relationship(
        'Er1Task',
        back_populates='attachment_is_attached',
        foreign_keys=[task_id]
    )
