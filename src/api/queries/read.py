from sqlalchemy_json_querybuilder.querybuilder.search import Search
from sqlalchemy import func, select


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

    def fetch_one(self, model, **kwargs):
        q = self._build_query(model, offset=0, limit=1, **kwargs)
        obj = q.first()
        if obj:
            return obj.__marshmallow__().dump(obj)
        else:
            return None
