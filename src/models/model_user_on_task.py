import sqlalchemy as sa

from models.base import Base

__all__ = ['UserOnTask']


class UserOnTask(Base):
    __tablename__ = 'user_on_task'
    __table_args__ = {"schema": "er1"}

    user_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.user.name', onupdate='cascade', ondelete='cascade'),
        primary_key=True
    )
    task_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.task.name', onupdate='cascade', ondelete='cascade'),
        primary_key=True
    )
