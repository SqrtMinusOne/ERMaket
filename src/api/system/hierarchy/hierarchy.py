from bs4 import BeautifulSoup

from api import Config
from utils.xml import XMLObject, xmlall

from .elements import Page, PrebuiltPage
from .form import Form
from .section import Section
from .table import Table

__all__ = ['Hierachy']

_Hierarchy = xmlall(
    '__Hierachy',
    'hierarchy',
    sections=Section,
    forms=Form,
    tables=Table,
    pages=Page,
    prebuiltPages=PrebuiltPage
)


class Hierachy(_Hierarchy):
    def __init__(self, xml=None):
        self._config = Config()
        if xml is not None:
            if isinstance(xml, BeautifulSoup):
                self.soup = xml
            else:
                self.soup = BeautifulSoup(xml, features='xml')
            args, kwargs = self._from_xml(self.soup.hierarchy)
            super().__init__(*args, **kwargs)
        else:
            self.soup = BeautifulSoup(features='xml')
            super().__init__()
            self.soup.append(
                self.soup.new_tag(
                    self._tag_name, **self._config.XML['HierarchyAttributes']
                )
            )
        XMLObject.soup = self.soup
        self.set_tree()

    def set_tree(self):
        self._set_ids()
        resolved = set()
        [
            [
                resolved.add(id.value)
                for id in section.resolve_children(self.get_by_id)
            ] for section in self.sections
        ]
        self._resolved = resolved
        self._root = [
            elem for elem in self.values if elem.id not in self._resolved
        ]
        self._resolve_rights()
        self._set_tables()

    def _set_ids(self):
        self._ids = {int(elem.id): elem for elem in self.elements}
        self._last_id = 0
        self._new_id()

    def _resolve_rights(self):
        for elem in self._root:
            if elem.accessRights.inherit:
                raise ValueError(
                    f'Element {elem} is root and cannot inherit accessRights'
                )
            if isinstance(elem, Section):
                elem.resolve_rights()

    def _set_tables(self):
        self._tables = {}
        for table in self.tables:
            try:
                self._tables[table.schema][table.tableName] = table
            except KeyError:
                self._tables[table.schema] = {table.tableName: table}

    def get_table_entry(self, schema, name):
        try:
            return self._tables[schema][name]
        except KeyError:
            return None

    def merge(self, other):
        map_ids = {}
        for elem in other.values:
            if elem.id in self._ids:
                map_ids[elem.id] = self._new_id()
                self._ids[map_ids[elem.id]] = None
            else:
                map_ids[elem.id] = elem.id
        for elem in other.values:
            elem.id = map_ids[elem.id]
            if isinstance(elem, Section):
                elem.map_ids(lambda id: map_ids[id])
        self.values.extend(other.values)
        self.set_tree()

    @classmethod
    def from_xml(cls, xml):
        return cls(xml)

    def to_xml(self):
        soup = BeautifulSoup(features='xml')
        tag = super().to_xml()
        for key, value in self._config.XML['HierarchyAttributes'].items():
            tag[key] = value
        soup.append(tag)
        return soup

    def to_object(self, *args, **kwargs):
        res = []
        for elem in self.values:
            res.append(elem.to_object())
        return {'hierarchy': res, 'root': [elem.id for elem in self._root]}

    def extract(self, roles):
        h = Hierachy()
        schemas = set()
        for table in self.tables:
            if len(table.accessRights.get(roles)) > 0:
                schemas.add(table.schema)
        for elem in self.values:
            if (
                len(elem.accessRights.get(roles)) > 0 or
                isinstance(elem, Table) and elem.schema in schemas
            ):
                h.append(elem)
        h.set_tree()
        return h

    def extract_rights(self, roles):
        rights = {}
        for elem in self.values:
            for right in elem.accessRights.get(roles):
                try:
                    rights[right.value].append(elem.id)
                except KeyError:
                    rights[right.value] = [elem.id]
        return rights

    def drop_by_id(self, id):
        self.values.remove(self._ids[id])
        del self._ids[id]

    def drop_schema(self, schema_name):
        self.values = [
            elem for elem in self.values if not any(
                [
                    isinstance(elem, Table) and elem.schema == schema_name,
                    isinstance(elem, Form) and
                    elem.formDescription.schema == schema_name
                ]
            )
        ]
        self.set_tree()

    @property
    def elements(self):
        return (
            *self.sections, *self.forms, *self.tables, *self.pages,
            *self.prebuiltPages
        )

    def get_by_id(self, id):
        try:
            if isinstance(id, XMLObject):
                return self._ids[id.value]
            return self._ids[id]
        except KeyError:
            return None

    def get_by_name(self, name):
        for value in self.values:
            if value.name == name:
                return name

    def _new_id(self):
        while self._last_id in self._ids:
            self._last_id += 1
        return self._last_id

    def append(self, elem):
        super().append(elem)
        if not hasattr(elem, 'id') or elem.id is None:
            elem.id = self._new_id()
        self._ids[elem.id] = elem
