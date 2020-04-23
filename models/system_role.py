# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

import sqlalchemy as sa
from .base import Base

__all__ = ['Role']


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'system'}

    name = sa.Column(sa.String(256), primary_key=True)
    is_default = sa.Column(sa.Boolean(), default=False)
    can_reset_password = sa.Column(sa.Boolean(), default=False)
    has_sql_access = sa.Column(sa.Boolean(), default=False)

    can_register_all = sa.Column(sa.Boolean(), default=False)
    can_register = sa.Column(sa.ARRAY(sa.String), nullable=True)

    linked_entity_schema = sa.Column(sa.String(256), nullable=True)
    linked_entity_name = sa.Column(sa.String(256), nullable=True)

    users = sa.orm.relationship(
        'User', secondary='system.user_has_roles', back_populates='roles'
    )
