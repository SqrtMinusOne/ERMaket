from api.database import DBConn
from api.models import Models

from .hierarchy_manager import HierachyManager

__all__ = ['UserManager']


class UserManager:
    def __init__(self):
        self.models = Models()
        self._User = self.models['system']['User']
        self._hierarchy_mgr = HierachyManager(save=False)
        DBConn()

    @property
    def hierarchy(self):
        return self._hierarchy_mgr.hierarchy

    def check_user(self, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            user = db.query(self._User).filter(self._User.login == login).first()
            if not user:
                return
            if not user.check_password(password):
                return
            return user

    def add_user(self, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            user = self._User(login=login)
            user.set_password(password)
            db.add(user)
            db.commit()
        return user

    def login_user(self, user, session):
        roles = [role.name for role in user.roles]
        hierarchy = self._hierarchy_mgr.hierarchy.extract(
            roles
        ).to_object()
        session['hierarchy'] = hierarchy
        session.modified = True
