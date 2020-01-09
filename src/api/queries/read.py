from sqlalchemy_json_querybuilder.querybuilder.search import Search


class QueryBuilder:
    def __init__(self, session):
        self._session = session

    def _build_query(self, model, page, per_page, **kwargs):
        search_obj = Search(
            self._session, model.__module_name__, (model, ), **kwargs
        )
        return search_obj.query().offset(per_page * page).limit(per_page)

    def fetch_data(self, model, page=0, per_page=10, **kwargs):
        q = self._build_query(model, page=page, per_page=per_page, **kwargs)
        result = self._session.execute(q.statement)
        serialized = [dict(row) for row in result]
        return serialized

    def fetch_one(self, model, **kwargs):
        q = self._build_query(model, page=0, per_page=1, **kwargs)
        obj = q.first()
        if obj:
            return obj.__marshmallow__().dump(obj)
        else:
            return None
