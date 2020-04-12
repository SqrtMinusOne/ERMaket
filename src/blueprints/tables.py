from collections import namedtuple

import simplejson as json
from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required

from api.database import DBConn
from api.models import Models, NamesConverter
from api.queries import QueryBuilder
from api.scripts import ServerScriptExecutor
from api.system import UserManager
from api.system.hierarchy import AccessRight, Activation

models = Models()
user_mgr = UserManager()
scripts = ServerScriptExecutor()

TableRequestInfo = namedtuple('TableRequestInfo', ['model'])

__all__ = ['tables']
tables = Blueprint('tables', 'tables')


def bind_criterion(criterion, name):
    criterion['field_name'] = name + '.' + criterion['field_name']


def get_filter_params(args, model_name, pagination=True, default_order=None):
    kwargs = {}
    kwargs['filter_by'] = json.loads(
        request.args.get('filter_by', default='[]', type=str)
    )
    default_order = json.dumps(
        default_order
    ) if default_order is not None else '[]'
    if isinstance(kwargs['filter_by'], dict):
        [
            [bind_criterion(criterion, model_name) for criterion in group]
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
            request.args.get('order_by', default=default_order, type=str)
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
    order = entry.get_default_sort()
    return entry, model, name, order


@tables.route('/table/<schema>/<table>')
@login_required
def get_table(schema, table):
    with DBConn.get_session() as db:
        entry, model, name, order = get_model(
            db, schema, table, AccessRight.VIEW
        )
        info = TableRequestInfo(model)
        if not scripts.process_logic(Activation.READ, entry, info):
            return scripts.return_

        kwargs = get_filter_params(request.args, name, default_order=order)
        builder = QueryBuilder(db)
        data = builder.fetch_data(model, **kwargs)
        result = {
            "data": data,
            "total": builder.count_data(model),
            **scripts.append_
        }
    return jsonify(result)


@tables.route('/entry/<schema>/<table>')
@login_required
def get_entry(schema, table):
    with DBConn.get_session() as db:
        entry, model, name, _ = get_model(db, schema, table, AccessRight.VIEW)
        info = TableRequestInfo(model)
        if not scripts.process_logic(Activation.READ, entry, info):
            return scripts.return_

        kwargs = get_filter_params(request.args, name, pagination=False)
        builder = QueryBuilder(db)
        result = builder.fetch_one(model, entry.displayColumns, **kwargs)
    return jsonify({**result, **scripts.append_})
