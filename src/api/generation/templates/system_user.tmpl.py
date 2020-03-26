import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .base import Base

__all__ = ['User']


class User(Base, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'system'}

    login = sa.Column(sa.String(256), primary_key=True)
    password_hash = sa.Column(sa.String(256), nullable=False)

    roles = sa.orm.relationship(
        'Role', secondary='system.user_has_roles', backref='users'
    )

    def change_password(self, old, new) -> bool:
        if self.check_password(old):
            self.set_password(new)
            return True
        return False

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def can_register(self, role_names):
        if any([role.can_register_all for role in self.roles]):
            return True
        target = set(role_names)
        authority = set()
        [
            authority.update(role.can_register)
            for role in self.roles if role.can_register is not None
        ]
        return len(target.difference(authority)) == 0

    def can_reset_password(self):
        return any([role.can_reset_password for role in self.roles])

    @property
    def role_names(self):
        return [role.name for role in self.roles]

    @property
    def is_active(self):
        return True  # All users are active

    @property
    def is_anonymous(self):
        return False  # TODO?

    def get_id(self):
        return self.login
