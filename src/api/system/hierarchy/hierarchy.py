from bs4 import BeautifulSoup

from api import Config
from api.erd.er_entities import XMLObject

from .elements import Page, PrebuiltPage
from .form import Form
from .section import Section
from .table import Table
from .xmlall import xmlall

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
        self._set_ids()
        self.set_tree()

    def set_tree(self):
        resolved = set()
        [
            [
                resolved.add(id)
                for id in section.resolve_children(self.get_by_id)
            ] for section in self.sections
        ]
        self._resolved = resolved

    def merge(self, other):
        self.values.extend(other.values)

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
            if elem._tag_name == 'Section' or elem.id not in self._resolved:
                res.append(elem.to_object())
        return {'hierarchy': res}

    @property
    def elements(self):
        return (
            *self.sections, *self.forms, *self.tables, *self.pages,
            *self.prebuiltPages
        )

    def _set_ids(self):
        self._ids = {int(elem.id): elem for elem in self.elements}
        self._last_id = 0
        self._new_id()

    def get_by_id(self, id):
        if isinstance(id, XMLObject):
            return self._ids[id.value]
        return self.ids[id]

    def _new_id(self):
        while self._last_id in self._ids:
            self._last_id += 1
        return self._last_id

    def append(self, elem):
        super().append(elem)
        elem.id = self._new_id()
        self._ids[elem.id] = elem
