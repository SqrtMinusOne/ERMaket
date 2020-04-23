import secrets
from datetime import datetime

import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from .base import Base

__all__ = ['Token']


class Token(Base):
    __tablename__ = 'token'
    __table_args__ = {'schema': 'system'}

    name = sa.Column(sa.String(256))
    token_hash = sa.Column(sa.String(256), primary_key=True)
    infinite = sa.Column(sa.Boolean(), default=False)
    uses = sa.Column(sa.Integer(), default=1)
    time_limit = sa.Column(sa.DateTime(), nullable=True)
    description = sa.Column(sa.JSON(), nullable=False)

    @property
    def valid(self):
        return (
            (self.time_limit is None or self.time_limit >= datetime.now()) and
            (self.infinite or self.uses > 0)
        )

    def use(self):
        if not self.infinite:
            self.uses -= 1

    def check_token(self, token):
        return check_password_hash(self.token_hash, token)

    def get_token(self):
        token = secrets.token_hex(32)
        self.token_hash = generate_password_hash(token, method='plain')
        return token
