from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required, login_user, logout_user

from api.database import DBConn
from api.system import UserManager

auth = Blueprint('auth', 'auth', url_prefix='/auth')
manager = UserManager()


@auth.route('/login', methods=['POST'])
def login():
    data = request.form
    with DBConn.get_session() as db:
        user = manager.check_user(data['login'], data['password'], db)
        if user:
            login_user(user)
            manager.login_user(user, session)
            return jsonify({"ok": True})
    return jsonify({"ok": False})


@auth.route('/current')
@login_required
def current():
    with DBConn.get_session() as sess:
        sess.add(current_user)
        obj = current_user.__marshmallow__().dump(current_user)
        obj['user_hierarchy'] = session.get('hierarchy')
    return jsonify(obj)


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True})
