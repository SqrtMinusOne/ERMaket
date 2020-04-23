from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_login import login_required

from ermaket.api.system.hierarchy import Activation
from ermaket.api.scripts import ServerScriptExecutor

scripts = ServerScriptExecutor()

__all__ = ['business_logic']
business_logic = Blueprint('business_logic', 'business_logic')
CORS(business_logic, supports_credentials=True)


@business_logic.route('/execute/<id>', methods=['POST'])
@login_required
def process(id):
    data = request.form or request.json
    try:
        activation = Activation(data['activation'])
    except (KeyError, TypeError):
        activation = Activation(Activation.CALL)
    if not scripts.process_call(int(id), activation):
        return scripts.return_
    return jsonify({"ok": True, **scripts.append_})
