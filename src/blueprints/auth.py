from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required

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
            return jsonify({"ok": True})
    return jsonify({"ok": False})


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True})
