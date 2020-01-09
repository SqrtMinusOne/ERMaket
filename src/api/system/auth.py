from api.database import DBConn
# from api.models import Models
from models import User


__all__ = ['UserManager']


class UserManager:
    def __init__(self):
        # self.models = Models()
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
