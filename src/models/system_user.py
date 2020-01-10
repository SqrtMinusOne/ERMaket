# This file was generated automatically and will be overwritten
# with next generation. Make changes with caution

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

    @property
    def is_active(self):
        return True  # All users are active

    @property
    def is_anonymous(self):
        return False  # TODO?

    def get_id(self):
        return self.login
