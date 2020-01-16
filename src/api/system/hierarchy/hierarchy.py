from bs4 import BeautifulSoup

from api import Config
from api.erd.er_entities import XMLObject

from .elements import Page, PrebuiltPage, Section
from .table import Table
from .form import Form
from .xmlall import xmlall

__all__ = ['Hierachy']

_Hierarchy = xmlall(
    '_Hierachy',
    'hierarchy',
    sections=Section,
    forms=Form,
    tables=Table,
    pages=Page,
    prebuiltPages=PrebuiltPage
)


class Hierachy(_Hierarchy):
    def __init__(self, xml):
        self._config = Config()
        if xml:
            self.soup = BeautifulSoup(xml, features='xml')
            super().__init__(self._from_xml(xml))
        else:
            self.soup = BeautifulSoup(features='xml')
            super().__init__()
            self.soup.append(
                self.soup.new_tag(
                    self._tag_name, **self._config.XML['HierarchyAttributes']
                )
            )
        XMLObject.soup = self.soup
        self.set_ids()

    @property
    def elements(self):
        return (
            *self.sections, *self.forms, *self.tables, *self.pages,
            *self.prebuiltPages
        )

    def _set_ids(self):
        self._ids = set(int(elem.id_) for elem in self.elements)
        self._last_id = 0
        self.new_id()

    def new_id(self):
        while self._last_id in self._ids:
            self._last_id += 1
        return self._last_id

    def next_id(self):
        ret = self.new_id()
        self._ids.add(ret)
        return ret
