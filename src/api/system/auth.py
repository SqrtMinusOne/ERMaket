from sqlalchemy.orm.exc import NoResultFound

from api.database import DBConn
from api.models import Models
from utils import Singleton

from .hierarchy_manager import HierachyManager

__all__ = ['UserManager']


def get_or_create(session, model, defaults=None, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        if defaults is not None:
            kwargs.update(defaults)
        with session.begin_nested():
            instance = model(**kwargs)
            session.add(instance)
            return instance


class UserManager(metaclass=Singleton):
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

    def add_roles(self, db, role_names=None):
        Role = self.models['system']['Role']
        roles = set(db.query(Role).filter(Role.is_default))
        if role_names:
            for name in role_names:
                roles.add(get_or_create(db, Role, name=name))
        return list(roles)

    def add_user(self, login, password, db=None, role_names=None):
        with DBConn.ensure_session(db) as db:
            user = self._User(login=login)
            user.set_password(password)
            db.add(user)
            roles = self.add_roles(db, role_names)
            user.roles = roles
            db.commit()
        return user

    def login_user(self, user, session):
        roles = [role.name for role in user.roles]
        extracted = self._hierarchy_mgr.hierarchy.extract(roles)
        session['hierarchy'] = extracted.to_object()
        session['rights'] = extracted.extract_rights(roles)
        session.modified = True
