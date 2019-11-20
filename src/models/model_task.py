import sqlalchemy as sa

from models.base import Base

__all__ = ['Task']


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {"schema": "er1"}

    name = sa.Column(sa.String(256), primary_key=True)
    finish_date = sa.Column(sa.DateTime, nullable=False, index=True)
    description = sa.Column(sa.Text, nullable=False)

    list_name = sa.Column(
        sa.String(256),
        sa.ForeignKey('er1.list.name', onupdate='cascade', ondelete='cascade')
    )
    attachment_on = sa.orm.relationship("Attachment", backref="task")
    subtask_on = sa.orm.relationship("Subtask", backref="task")
    user_on = sa.orm.relationship("UserOnTask", backref="task")
