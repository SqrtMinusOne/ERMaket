from typing import List

from bs4 import BeautifulSoup

from api.erd.er_entities import Entity, Relation, XMLObject

__all__ = ['ERD']


class ERD:
    def __init__(self, xml):
        self.soup = BeautifulSoup(xml, 'xml')
        XMLObject.soup = self.soup

        self.entities: List[Entity] = []
        self.relations: List[Relation] = []

        self._parse_xml()

    def _parse_xml(self):
        self.entities = [
            Entity.from_xml(tag) for tag in self.soup.find_all('entity')
        ]
        self.relations = [
            Relation.from_xml(tag) for tag in self.soup.find_all('relation')
        ]
