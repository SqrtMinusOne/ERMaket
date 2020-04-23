from flask import Blueprint, session, abort, request, jsonify
from flask_login import login_required

from ermaket.api.queries import SqlExecutor

__all__ = ['sql']
sql = Blueprint('sql', 'sql')

executor = SqlExecutor()


@sql.route('/execute', methods=['POST'])
@login_required
def execute():
    sql_user = session.get('sql_user')
    if sql_user is None:
        abort(403)
    data = request.json
    res, keys = executor.execute(data['query'], user=sql_user)
    return jsonify({"ok": True, "result": res, "keys": keys})
