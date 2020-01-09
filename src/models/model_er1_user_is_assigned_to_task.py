import sqlalchemy as sa

from .base import Base

__all__ = ['Er1UserIsAssignedToTask']


class Er1UserIsAssignedToTask(Base):
    __tablename__ = 'user_is_assigned_to_task'
    __table_args__ = {'schema': 'er1'}

    user_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.user.name', ondelete='cascade', onupdate='cascade'),
        primary_key=True,
        unique=True
    )
    task_id = sa.Column(
        sa.BigInteger(),
        sa.ForeignKey('er1.task.id', ondelete='cascade', onupdate='cascade'),
        primary_key=True,
        unique=True
    )
