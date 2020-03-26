import logging

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash

from api.database import DBConn
from api.models import Models, NamesConverter
from api.system.hierarchy import AccessRight, PrebuiltPageType
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
        self._Token = self.models['system']['Token']
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

    def add_register_token(self, *args, roles=None, **kwargs):
        if roles is None:
            roles = []
        description = {'purpose': 'registration', 'roles': roles}
        return self._add_token(*args, description, **kwargs)

    def add_reset_password_token(self, name, login, **kwargs):
        description = {'purpose': 'password', 'login': login}
        return self._add_token(name, description, **kwargs)

    def _add_token(
        self,
        name,
        description,
        roles=None,
        uses=None,
        time_limit=None,
        db=None
    ):
        with DBConn.ensure_session(db) as db:
            token_obj = self._Token(
                name=name,
                infinite=uses is None,
                uses=uses,
                time_limit=time_limit,
                description=description
            )
            token_hash = token_obj.get_token()
            db.add(token_obj)
            db.commit()
        return token_hash

    def register_user(self, token, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            token_hash = generate_password_hash(token, method='plain')
            token = db.query(self._Token).get(token_hash)
            if (
                token is None or not token.valid or
                not token.description['purpose'] == 'registration'
            ):
                return None
            user = self.add_user(
                login, password, role_names=token.description['roles'], db=db
            )
            if user is not None:
                token.use()
                db.commit()
        return user

    def reset_password(self, token, login, password, db=None):
        with DBConn.ensure_session(db) as db:
            token_hash = generate_password_hash(token, method='plain')
            token = db.query(self._Token).get(token_hash)
            if (
                token is None or not token.valid or
                not token.description['purpose'] == 'password'
                or token.description['login'] != login
            ):
                return False
            user = db.query(self._User).get(login)
            user.set_password(password)
            token.use()
            db.commit()
        return True

    def add_role(self, db=None, **kwargs):
        Role = self.models['system']['Role']
        with DBConn.ensure_session(db) as db:
            role = Role(**kwargs)
            db.add(role)
            db.commit()
        return role

    def login_user(self, user, session):
        roles = [role.name for role in user.roles]
        extracted = self._hierarchy_mgr.hierarchy.extract(roles)
        session['hierarchy'] = extracted.to_object()
        session['rights'] = extracted.extract_rights(roles)
        session['profile_forms'] = self._extract_profile_forms(user)
        self._set_sql(user, session, extracted)
        session.modified = True

    def _extract_profile_forms(self, user):
        models = [
            self.models[role.linked_entity_schema][NamesConverter.class_name(
                role.linked_entity_schema, role.linked_entity_name
            )] for role in user.roles if role.linked_entity_name is not None
        ]
        return [
            self._hierarchy_mgr.hierarchy.get_table_entry(
                model.__table__.schema, model.__tablename__
            ).formDescription.to_object() for model in models
        ]

    def _set_sql(self, user, session, extracted):
        roles = [role.name for role in user.roles]
        has_sql = any([role.has_sql_access for role in user.roles])
        if not has_sql:
            return

        sql_page = next(
            (
                page for page in extracted.prebuiltPages
                if page.type == PrebuiltPageType.SQL
            ), None
        )
        if sql_page is None:
            logging.warn(
                f'User {user} is set to have sql access, but has no sql'
                'console page in the hirerarchy'
            )
        else:
            if sql_page.accessRights.has(roles, AccessRight.CHANGE):
                session['sql_user'] = 'sql'
            elif sql_page.accessRights.has(roles, AccessRight.VIEW):
                session['sql_user'] = 'view'
