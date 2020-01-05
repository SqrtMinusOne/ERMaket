from typing import List, Dict

from api.erd.er_entities import Entity, Relation, XMLObject
from bs4 import BeautifulSoup

__all__ = ['ERD']


class ERD:
    def __init__(self, xml):
        self.soup = BeautifulSoup(xml, 'xml')
        XMLObject.soup = self.soup

        self.entities: Dict[int, Entity] = {}
        self.relations: List[Relation] = []

        self._parse_xml()

    def _parse_xml(self):
        for tag in self.soup.find_all('entity'):
            entity = Entity.from_xml(tag)
            self.entities[entity._id] = entity

        self.relations = [
            Relation.from_xml(tag) for tag in self.soup.find_all('relation')
        ]
