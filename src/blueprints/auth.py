from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_cors import CORS

from api.database import DBConn
from api.system import UserManager

__all__ = ['auth']

auth = Blueprint('auth', 'auth', url_prefix='/auth')
CORS(auth, supports_credentials=True)

manager = UserManager()


@auth.route('/login', methods=['POST'])
def login():
    data = request.form or request.json
    with DBConn.get_session() as db:
        user = manager.check_user(data['login'], data['password'], db)
        if user:
            manager.login_user(user, session)
            login_user(user)
            return jsonify({"ok": True})
    return jsonify({"ok": False}), 401


@auth.route('/current')
@login_required
def current():
    with DBConn.get_session() as sess:
        sess.add(current_user)
        user = current_user.__marshmallow__().dump(current_user)
        return jsonify({
            "ok": True,
            "user": user,
            "hierarchy": session.get('hierarchy'),
            "rights": session.get('rights')
        })


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True})
