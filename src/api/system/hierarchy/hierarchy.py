from bs4 import BeautifulSoup

from api import Config
from api.erd.er_entities import XMLObject

from .elements import Page, PrebuiltPage, Section
from .form import Form
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

    @property
    def elements(self):
        return (
            *self.sections, *self.forms, *self.tables, *self.pages,
            *self.prebuiltPages
        )

    def _set_ids(self):
        self._ids = set(int(elem.id) for elem in self.elements)
        self._last_id = 0
        self._new_id()

    def _new_id(self):
        while self._last_id in self._ids:
            self._last_id += 1
        return self._last_id

    def _next_id(self):
        ret = self._new_id()
        self._ids.add(ret)
        return ret
