import sqlalchemy as sa

from models.base import Base

__all__ = ['Attachment']


class Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = {"schema": "er1"}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    filePath = sa.Column(sa.String(512), nullable=False)

    task_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.task.name', onupdate='cascade', ondelete='cascade')
    )
