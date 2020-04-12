import os
import traceback
from collections import namedtuple

from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_login import login_required

from api.database import DBConn
from api.queries import ErrorsParser, Transaction
from api.scripts import ServerScriptExecutor
from api.system.hierarchy import Activation

scripts = ServerScriptExecutor()

TransactionRequestInfo = namedtuple('TransactionRequestInfo', ['transaction'])

__all__ = ['transaction']
transaction = Blueprint(
    'transaction', 'transaction'
)
CORS(transaction, supports_credentials=True)


@transaction.route('/execute', methods=['POST'])
@login_required
def process():
    data = request.form or request.json
    with DBConn.get_session(autoflush=False) as db:
        transaction = Transaction(db, data['transaction'])
        info = TransactionRequestInfo(transaction)
        if not scripts.process_global(Activation.TRANSACTION, info):
            return scripts.return_

        try:
            transaction.execute()
        except Exception as exp:
            error, code = ErrorsParser.parse(exp)
            response = {
                "ok": False,
                "message": error.message,
                "data": error.info
            }
            if os.environ.get('FLASK_ENV') == 'development':
                response['traceback'] = traceback.format_exc()
            return jsonify(response), code
    return jsonify({"ok": True, **scripts.append_})
