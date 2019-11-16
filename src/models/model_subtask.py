import sqlalchemy as sa

from models.base import Base

__all__ = ['Subtask']


class Subtask(Base):
    __tablename__ = 'subtask'
    __table_args__ = {"schema": "er1"}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(256), nullable=False)

    task_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.task.name', onupdate='cascade', ondelete='cascade')
    )

    item_on = sa.orm.relationship('Item', backref="subtask")
