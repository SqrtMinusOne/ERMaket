from flask import Blueprint, jsonify, request, session
from flask_cors import CORS
from flask_login import current_user, login_required, login_user, logout_user

from api.database import DBConn
from api.scripts import ServerScriptExecutor
from api.system import UserManager
from api.system.hierarchy import Activation

__all__ = ['auth']

auth = Blueprint('auth', 'auth', url_prefix='/auth')
CORS(auth, supports_credentials=True)

manager = UserManager()
scripts = ServerScriptExecutor()


@auth.route('/login', methods=['POST'])
def login():
    data = request.form or request.json
    if not scripts.process_global(Activation.LOGIN):
        return scripts.return_
    with DBConn.get_session() as db:
        user = manager.check_user(data['login'], data['password'], db)
        if user:
            manager.login_user(user, session)
            login_user(user)
            return jsonify({"ok": True, **scripts.append_})
    return jsonify(
        {
            "ok": False,
            "message": "Incorrect username or password",
            **scripts.append_
        }
    ), 401


@auth.route('/current')
@login_required
def current():
    with DBConn.get_session() as sess:
        sess.add(current_user)
        user = current_user.__marshmallow__().dump(current_user)
        return jsonify(
            {
                "ok": True,
                "user": user,
                "hierarchy": session.get('hierarchy'),
                "rights": session.get('rights'),
                "profile_forms": session.get('profile_forms')
            }
        )


@auth.route('/password', methods=['POST'])
@login_required
def password():
    data = request.form or request.json
    with DBConn.get_session() as sess:
        sess.add(current_user)
        success = current_user.change_password(
            data['old_pass'], data['new_pass']
        )
        if success:
            sess.commit()
    return jsonify({"ok": success})


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    if not scripts.process_global(Activation.LOGIN):
        return scripts.return_
    logout_user()
    return jsonify({"ok": True, **scripts.append_})
