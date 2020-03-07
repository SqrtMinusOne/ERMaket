from magic_repr import make_repr

from api.config import Config
from api.models import Models, NamesConverter
from api.system import HierachyManager
from api.system.hierarchy import AccessRight

__all__ = ['Transaction', 'InsufficientRightsError']


class InsufficientRightsError(Exception):
    def __init__(self, target, right):
        self.target = target
        self.right = right

    def __str__(self):
        return f'No {self.right} access for {self.target}'


InsufficientRightsError.__repr__ = make_repr('target', 'right')


class Transaction:
    def __init__(self, session, params, role_names=None):
        self._db = session
        self._params = params
        self._role_names = role_names

        self._models = Models()
        self._hierarchy = HierachyManager()
        self._config = Config()

        self._extracted = {}
        self._tables = {}
        self._pks = {}

    def execute(self):
        self._prepare()
        self._check_rights()
        try:
            for _id in self._params.keys():
                self._process_id(_id)
            self._db.commit()
        except Exception as exp:
            self._db.rollback()
            raise exp

    def _prepare(self):
        self._params = {int(_id): unit for _id, unit in self._params.items()}
        for _id in self._params.keys():
            table = self._hierarchy.h.get_by_id(_id)
            name = NamesConverter.class_name(table.schema, table.tableName)
            model = self._models[table.schema][name]
            self._extracted[_id] = model
            self._tables[_id] = table

            self._pks[_id] = table.pk

    def _check_rights(self):
        if self._role_names is None:
            return
        for _id in self._params.keys():
            rights = self._tables[_id].accessRights
            if (
                self._has_entry(_id, 'create') or
                self._has_entry(_id, 'update')
            ) and not rights.has(self._role_names, AccessRight.CHANGE):
                raise InsufficientRightsError(
                    self._tables[_id], AccessRight.CHANGE
                )
            if (
                self._has_entry(_id, 'delete') and
                not rights.has(self._role_names, AccessRight.DELETE)
            ):
                raise InsufficientRightsError(
                    self._tables[_id], AccessRight.DELETE
                )

    def _has_entry(self, _id, name):
        return (name in self._params[_id] and len(self._params[_id][name]) > 0)

    def _process_id(self, _id):
        if 'create' in self._params[_id]:
            self._process_create(_id)
        if 'delete' in self._params[_id]:
            self._process_delete(_id)
        if 'update' in self._params[_id]:
            self._process_update(_id)

    def _process_create(self, _id):
        pk = self._pks[_id]
        model = self._extracted[_id]

        for data in self._params[_id]['create'].values():
            kwargs = data['newData']
            if pk.isAuto:
                try:
                    del kwargs[pk.rowName]
                except KeyError:
                    pass

            obj = model.__marshmallow__().load(kwargs, session=self._db)
            self._db.add(obj)

    def _process_delete(self, _id):
        pk = self._pks[_id]
        model = self._extracted[_id]

        for key in self._params[_id]['delete'].keys():
            self._db.query(model).filter_by(**{pk.rowName: key}).delete()

    def _process_update(self, _id):
        model = self._extracted[_id]
        pk = self._pks[_id]
        for update in self._params[_id]['update'].values():

            # TODO Optimize?
            item = self._db.query(model).filter_by(
                **{
                    pk.rowName: update['oldData'][pk.rowName]
                }
            ).first()
            new_item = model.__marshmallow__().load(
                {
                    **update['oldData'],
                    **update['newData']
                },
                session=self._db,
                instance=item
            )
            self._db.add(new_item)
