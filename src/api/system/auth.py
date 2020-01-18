from api.database import DBConn
from models import User

from .hierarchy_manager import HierachyManager

__all__ = ['UserManager']


class UserManager:
    def __init__(self):
        # self.models = Models()
        self._hierarchy_mgr = HierachyManager()
        DBConn()

    def check_user(self, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            user = db.query(User).filter(User.login == login).first()
            if not user:
                return
            if not user.check_password(password):
                return
            return user

    def add_user(self, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            user = User(login=login)
            user.set_password(password)
            db.add(user)
            db.commit()

    def login_user(self, user):
        user.user_hierarchy = self._hierarchy_mgr.hierarchy.extract(
            user.roles
        ).to_object()
