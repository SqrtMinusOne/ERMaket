import sqlalchemy as sa
from .system_base import Base


__all__ = ['Role']


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'system'}

    name = sa.Column(sa.String(256), primary_key=True)
    can_reset_password = sa.Column(sa.Boolean(), default=False)
    has_sql_access = sa.Column(sa.Boolean(), default=False)
