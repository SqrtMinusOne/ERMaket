from flask import Blueprint, abort, jsonify, request, session
from flask_cors import CORS
from flask_login import current_user, login_required, login_user, logout_user

from api.database import DBConn
from api.scripts import ReturnContext, ServerScriptExecutor
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


@auth.route('/password', methods=['PUT'])
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


@auth.route('/reset_password', methods=['PUT'])
def reset_password():
    data = request.form or request.json
    success = manager.reset_password(
        data['token'], data['login'], data['password']
    )
    return jsonify({"ok": success})


@auth.route('/register', methods=['POST'])
def register():
    data = request.form or request.json
    user = manager.register_user(
        data['token'], data['login'], data['password']
    )
    ctx = ReturnContext()
    if user is None:
        ctx.add_message('Registration error', variant="danger")
        return jsonify({"ok": False, "businessLogic": ctx.append_request})
    if not scripts.process_global(Activation.LOGIN):
        return scripts.return_
    with DBConn.get_session() as db:
        db.add(user)
        manager.login_user(user, session)
        login_user(user)
    return jsonify({"ok": True, **scripts.append_})


@auth.route('/register_token', methods=['POST'])
@login_required
def register_token():
    data = request.form or request.json
    with DBConn.get_session() as sess:
        sess.add(current_user)
        if not current_user.can_register(data.get('roles', [])):
            abort(403)
        token = manager.add_register_token(
            name=data['name'],
            roles=data.get('roles', []),
            uses=data.get('uses', 1),
            time_limit=data.get('time_limit', None)
        )
    ctx = ReturnContext()
    ctx.add_message(
        f"""
        Registration token: <pre>{token}</pre><br>
        The token won't be shown anywhere except this message.
        """
    )
    return jsonify(
        {
            "ok": True,
            "token": token,
            "businessLogic": ctx.append_request
        }
    )


@auth.route('/reset_password_token', methods=['POST'])
@login_required
def reset_password_token():
    data = request.form or request.json
    with DBConn.get_session() as sess:
        sess.add(current_user)
        if not current_user.can_reset_password():
            abort(403)
        token = manager.add_reset_password_token(
            name=data['name'],
            login=data['login'],
            uses=data.get('uses', 1),
            time_limit=data.get('time_limit', None)
        )
    ctx = ReturnContext()
    ctx.add_message(
        f"""
        Reset password token: <pre>{token}</pre><br>
        The token won't be shown anywhere except this message.
        """
    )
    return jsonify(
        {
            "ok": True,
            "token": token,
            "businessLogic": ctx.append_request
        }
    )


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    if not scripts.process_global(Activation.LOGIN):
        return scripts.return_
    logout_user()
    return jsonify({"ok": True, **scripts.append_})
