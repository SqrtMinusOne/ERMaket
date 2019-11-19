from flask import abort, request
import json

from app import app, models
from api.database import DBConn
from api.models import NamesConverter


@app.route('/table/<schema>/<table>')
def get_table(schema, table):
    try:
        model = models[schema][NamesConverter.table_to_class(schema, table)]
    except KeyError:
        abort(404)
    filter = json.loads(request.args.get('filter', default='{}', type=str))
    page = request.args.get('page', default=0, type=int)
