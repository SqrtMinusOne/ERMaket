import sqlalchemy as sa

from .base import Base

__all__ = ['Er1User']


class Er1User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'er1'}

    name = sa.Column(
        sa.String(256),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False
    )

    comment_is_authored_by = sa.orm.relationship(
        'Er1Comment', back_populates='is_authored_by_user'
    )

    is_assigned_to_task = sa.orm.relationship(
        'Er1Task',
        secondary='er1.user_is_assigned_to_task',
        back_populates='is_assigned_to_user'
    )
