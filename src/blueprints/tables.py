import simplejson as json
from flask import Blueprint, abort, jsonify, request
from flask_login import login_required, current_user
from flask_cors import CORS

from api.database import DBConn
from api.models import Models, NamesConverter
from api.queries import QueryBuilder
from api.system import UserManager
from api.system.hierarchy import AccessRight

models = Models()
user_mgr = UserManager()

__all__ = ['tables']
tables = Blueprint('tables', 'tables', url_prefix='/tables')
CORS(tables)


def get_filter_params(args, pagination=True):
    kwargs = {}
    kwargs['filter_by'] = json.loads(
        request.args.get('filter_by', default='[]', type=str)
    )

    if pagination:
        kwargs['page'] = request.args.get('page', default=0, type=int)
        kwargs['per_page'] = request.args.get('per_page', default=10, type=int)
        kwargs['order_by'] = json.loads(
            request.args.get('order_by', default='[]', type=str)
        )
    return kwargs


def get_model(db, schema, table, access_type):
    entry = user_mgr.hierarchy.get_table_entry(schema, table)
    if entry is None:
        abort(404)
    db.add(current_user)
    if not entry.accessRights.has(current_user.role_names, access_type):
        abort(403)
    model = models[schema][NamesConverter.class_name(schema, table)]
    return model


@tables.route('/table/<schema>/<table>')
@login_required
def get_table(schema, table):
    with DBConn.get_session() as db:
        model = get_model(db, schema, table, AccessRight.VIEW)
        kwargs = get_filter_params(request.args)
        builder = QueryBuilder(db)
        result = builder.fetch_data(model, **kwargs)
    return jsonify(result)


@tables.route('/entry/<schema>/<table>')
@login_required
def get_entry(schema, table):
    with DBConn.get_session() as db:
        model = get_model(db, schema, table, AccessRight.VIEW)
        kwargs = get_filter_params(request.args, pagination=False)
        builder = QueryBuilder(db)
        result = builder.fetch_one(model, **kwargs)
    return jsonify(result)
