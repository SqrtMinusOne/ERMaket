import sqlalchemy as sa

from .base import Base

__all__ = ['Er1List']


class Er1List(Base):
    __tablename__ = 'list'
    __table_args__ = {'schema': 'er1'}

    id = sa.Column(
        sa.BigInteger(),
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True
    )
    name = sa.Column(
        sa.String(256),
        primary_key=False,
        nullable=False,
        unique=False,
        autoincrement=False
    )

    task_belongs_to = sa.orm.relationship(
        'Er1Task', back_populates='belongs_to_list'
    )
