import sqlalchemy as sa

from .base import Base

__all__ = ['UserHasRoles']


class UserHasRoles(Base):
    __tablename__ = 'user_has_roles'
    __table_args__ = {'schema': 'system'}
    login = sa.Column(
        sa.String(256),
        sa.ForeignKey(
            'system.user.login',
            deferrable=True,
            initially="DEFERRED",
            onupdate="cascade",
            ondelete="cascade"
        ),
        primary_key=True,
    )
    role = sa.Column(
        sa.String(256),
        sa.ForeignKey(
            'system.role.name',
            deferrable=True,
            initially="DEFERRED",
            onupdate="cascade",
            ondelete="cascade"
        ),
        primary_key=True,
    )
