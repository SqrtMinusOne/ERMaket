from sqlalchemy_json_querybuilder.querybuilder.search import Search


class QueryBuilder:
    def __init__(self, session):
        self._session = session

    def fetch_data(self, model, **kwargs):
        search_obj = Search(
            self._session, model.__module_name__, (model,), **kwargs)
