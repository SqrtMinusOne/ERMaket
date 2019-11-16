import sqlalchemy as sa

from models.base import Base

__all__ = ['Item']


class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {"schema": "er1"}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(256), nullable=False)

    subtask_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('er1.subtask.id', onupdate='cascade', ondelete='cascade')
    )
