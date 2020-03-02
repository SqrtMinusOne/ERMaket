from flask import Blueprint
from flask_cors import CORS
from flask_login import login_required


transaction = Blueprint('transaction', 'transaction', url_prefix='/change')
CORS(transaction, supports_credentials=True)

__all__ = []
