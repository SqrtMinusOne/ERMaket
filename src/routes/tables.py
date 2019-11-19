from flask import abort, request, jsonify
import simplejson as json

from app import app, models
from api.database import DBConn
from api.models import NamesConverter
from api.queries import QueryBuilder


def get_filter_params(args, pagination=True):
    kwargs = {}
    kwargs['filter_by'] = json.loads(
        request.args.get('filter_by', default='[]', type=str))

    if pagination:
        kwargs['page'] = request.args.get('page', default=1, type=int)
        kwargs['per_page'] = request.args.get('per_page', default=10, type=int)
        kwargs['order_by'] = json.loads(
            request.args.get('order_by', default='[]', type=str))
    return kwargs


@app.route('/table/<schema>/<table>')
def get_table(schema, table):
    try:
        model = models[schema][NamesConverter.table_to_class(schema, table)]
    except KeyError:
        abort(404)
    kwargs = get_filter_params(request.args)
    with DBConn.get_session() as session:
        builder = QueryBuilder(session)
        result = builder.fetch_data(model, **kwargs)
    return jsonify(result)


@app.route('/entry/<schema>/<table>')
def get_entry(schema, table):
    try:
        model = models[schema][NamesConverter.table_to_class(schema, table)]
    except KeyError:
        abort(404)
    kwargs = get_filter_params(request.args, pagination=False)
    with DBConn.get_session() as session:
        builder = QueryBuilder(session)
        result = builder.fetch_one(model, **kwargs)
    return jsonify(result)
