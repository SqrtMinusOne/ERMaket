from sqlalchemy import func, select
from sqlalchemy_json_querybuilder.querybuilder.search import Search

__all__ = ['QueryBuilder']


class QueryBuilder:
    def __init__(self, session):
        self._session = session

    def _build_query(self, model, offset, limit, **kwargs):
        search_obj = Search(
            self._session, model.__module_name__, (model, ), **kwargs
        )
        result = search_obj.query()
        if offset >= 0:
            result = result.offset(offset)
        if limit >= 0:
            result = result.limit(limit)
        return result

    def fetch_data(self, model, offset=0, limit=10, **kwargs):
        q = self._build_query(model, offset=offset, limit=limit, **kwargs)
        result = self._session.execute(q.statement)
        serialized = [dict(row) for row in result]
        return serialized

    def count_data(self, model):
        s = select([func.count()]).select_from(model.__table__)
        return self._session.execute(s).scalar()

    def fetch_one(self, model, display_columns=None, **kwargs):
        if display_columns is None:
            display_columns = []
        q = self._build_query(model, offset=0, limit=1, **kwargs)
        obj = q.first()
        if obj:
            dump = obj.__marshmallow__().dump(obj)

            _display = {}
            for attr_name, target_field, is_multiple in display_columns:
                attr = getattr(obj, attr_name)
                try:
                    _display[attr_name] = [
                        getattr(elem, target_field) for elem in attr
                    ]

                    if not is_multiple and len(_display[attr_name]) == 1:
                        _display[attr_name] = _display[attr_name][0]

                except TypeError:
                    _display[attr_name] = getattr(attr, target_field)

            dump["_display"] = _display
            return dump
        else:
            return None
