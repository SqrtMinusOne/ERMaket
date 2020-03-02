from api.models import Models, NamesConverter
from api.config import Config
from api.system import HierachyManager

__all__ = ['Transaction']


class Transaction:
    def __init__(self, session, params):
        self._db = session
        self._params = params

        self._models = Models()
        self._hierarchy = HierachyManager()
        self._config = Config()

        self._extracted = {}
        self._tables = {}
        self._pks = {}

    def execute(self):
        self._prepare()
        try:
            for _id in self._params.keys():
                self._process_id(_id)
            self._db.commit()
        except Exception as exp:
            self._db.rollback()
            raise exp

    def _prepare(self):
        for _id in self._params.keys():
            table = self._hierarchy.h.get_by_id(_id)
            name = NamesConverter.class_name(table.schema, table.tableName)
            model = self._models[table.schema][name]
            self._extracted[_id] = model
            self._tables[_id] = table

            self._pks[_id] = table.pk

    def _process_id(self, _id):
        self._process_create(_id)

    def _process_create(self, _id):
        pk = self._pks[_id]
        model = self._extracted[_id]

        for data in self._params[_id]['create'].values():
            kwargs = data['newData']
            if pk.isAuto:
                del kwargs[pk.rowName]

            obj = model(**kwargs)
            self._db.add(obj)

    def _process_update(self, _id):
        pass  # TODO

    def _process_delete(self, _id):
        pass
