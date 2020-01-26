import simplejson as json
from flask import Blueprint, abort, jsonify, request
from flask_login import login_required, current_user

from api.database import DBConn
from api.models import Models, NamesConverter
from api.queries import QueryBuilder
from api.system import UserManager
from api.system.hierarchy import AccessRight

models = Models()
user_mgr = UserManager()

__all__ = ['tables']
tables = Blueprint('tables', 'tables', url_prefix='/tables')


def bind_criterion(criterion, name):
    criterion['field_name'] = name + '.' + criterion['field_name']


def get_filter_params(args, model_name, pagination=True):
    kwargs = {}
    kwargs['filter_by'] = json.loads(
        request.args.get('filter_by', default='[]', type=str)
    )
    if isinstance(kwargs['filter_by'], dict):
        [
            [
                bind_criterion(criterion, model_name)
                for criterion in group
            ]
            for group in kwargs['filter_by'].values()
        ]
    elif isinstance(kwargs['filter_by'], list):
        [
            bind_criterion(criterion, model_name)
            for criterion in kwargs['filter_by']
        ]

    if pagination:
        kwargs['offset'] = request.args.get('offset', default=0, type=int)
        kwargs['limit'] = request.args.get('limit', default=10, type=int)
        kwargs['order_by'] = json.loads(
            request.args.get('order_by', default='[]', type=str)
        )
        for i in range(len(kwargs['order_by'])):
            order = kwargs['order_by'][i]
            if order.startswith('-'):
                kwargs['order_by'][i] = f"-{model_name}.{order[1:]}"
            else:
                kwargs['order_by'][i] = f"{model_name}.{order}"
    return kwargs


def get_model(db, schema, table, access_type):
    entry = user_mgr.hierarchy.get_table_entry(schema, table)
    if entry is None:
        abort(404)
    db.add(current_user)
    if not entry.accessRights.has(current_user.role_names, access_type):
        abort(403)
    name = NamesConverter.class_name(schema, table)
    model = models[schema][name]
    return model, name


@tables.route('/table/<schema>/<table>')
@login_required
def get_table(schema, table):
    with DBConn.get_session() as db:
        model, name = get_model(db, schema, table, AccessRight.VIEW)
        kwargs = get_filter_params(request.args, name)
        builder = QueryBuilder(db)
        data = builder.fetch_data(model, **kwargs)
        result = {
            "data": data,
            "total": builder.count_data(model)
        }
    return jsonify(result)


@tables.route('/entry/<schema>/<table>')
@login_required
def get_entry(schema, table):
    with DBConn.get_session() as db:
        model, name = get_model(db, schema, table, AccessRight.VIEW)
        kwargs = get_filter_params(request.args, name, pagination=False)
        builder = QueryBuilder(db)
        result = builder.fetch_one(model, **kwargs)
    return jsonify(result)
