from bs4 import BeautifulSoup

from api import Config
from api.erd.er_entities import XMLObject

from .section import Section
from .table import Table

__all__ = ['Hierachy']


class Hierachy:
    def __init__(self, xml=None):
        self._config = Config()
        if xml is not None:
            self.soup = BeautifulSoup(xml, 'xml')
        else:
            self.soup = BeautifulSoup(features='xml')
            self.soup.append(
                self.soup.new_tag(
                    'hierarchy', **self._config.XML['HierachyRootAttributes']
                )
            )
        XMLObject.soup = self.soup
        self.entries = []

        self._parse_xml()

    def _parse_xml(self):
        for tag in self.soup.hierarchy.children:
            if tag.name == 'table':
                self.entries.append(Table.from_xml(tag))
            if tag.name == 'section':
                self.entries.append(Section.from_xml(tag))
