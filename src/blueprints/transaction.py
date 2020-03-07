from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_login import login_required

from api.database import DBConn
from api.queries import ErrorsParser, Transaction

__all__ = ['transaction']

transaction = Blueprint(
    'transaction', 'transaction', url_prefix='/transaction'
)
CORS(transaction, supports_credentials=True)


@transaction.route('/execute', methods=['POST'])
@login_required
def process():
    data = request.form or request.json
    with DBConn.get_session() as db:
        transaction = Transaction(db, data['transaction'])
        try:
            transaction.execute()
        except Exception as exp:
            error, code = ErrorsParser.parse(exp)
            return jsonify(
                {
                    "ok": False,
                    "message": "Transaction error",
                    "data": error._asdict()
                }
            ), code
    return jsonify({"ok": True})
