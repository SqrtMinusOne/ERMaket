import sqlalchemy as sa
from .base import Base


__all__ = ['Role']


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'system'}

    name = sa.Column(sa.String(256), primary_key=True)
    can_reset_password = sa.Column(sa.Boolean(), default=False)
    has_sql_access = sa.Column(sa.Boolean(), default=False)
    linked_entity_schema = sa.Column(sa.String(256), nullable=True)
    linked_entity_id = sa.Column(sa.Integer(), nullable=True)
