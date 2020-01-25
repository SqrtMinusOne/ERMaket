from sqlalchemy_json_querybuilder.querybuilder.search import Search


class QueryBuilder:
    def __init__(self, session):
        self._session = session

    def _build_query(self, model, offset, limit, **kwargs):
        search_obj = Search(
            self._session, model.__module_name__, (model, ), **kwargs
        )
        return search_obj.query().offset(offset).limit(limit)

    def fetch_data(self, model, offset=0, limit=10, **kwargs):
        q = self._build_query(model, offset=offset, limit=limit, **kwargs)
        result = self._session.execute(q.statement)
        serialized = [dict(row) for row in result]
        return serialized

    def fetch_one(self, model, **kwargs):
        q = self._build_query(model, offset=0, limit=1, **kwargs)
        obj = q.first()
        if obj:
            return obj.__marshmallow__().dump(obj)
        else:
            return None
