import sqlalchemy as sa

from models.base import Base

__all__ = ['List']


class List(Base):
    __tablename__ = 'list'
    __table_args__ = {"schema": "er1"}

    name = sa.Column(sa.String(256), primary_key=True)

    task_on = sa.orm.relationship("Task", backref="list")
