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
        User = self._User
        with DBConn.ensure_session(db) as db:
            user = db.query(User).filter(User.login == login).first()
            if not user:
                return
            if not user.check_password(password):
                return
            return user

    def add_user(self, login, password, db=None):
        Role = self.models['system']['Role']
        with DBConn.ensure_session(db) as db:
            user = self._User(login=login)
            user.set_password(password)
            db.add(user)
            roles = db.query(Role).filter(Role.is_default)
            user.roles = list(roles)
            db.commit()
        return user

    def login_user(self, user, session):
        roles = [role.name for role in user.roles]
        extracted = self._hierarchy_mgr.hierarchy.extract(roles)
        session['hierarchy'] = extracted.to_object()
        session['rights'] = extracted.extract_rights(roles)
        session.modified = True
