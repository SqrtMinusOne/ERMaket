from typing import Dict, List

from bs4 import BeautifulSoup
from magic_repr import make_repr

from api.erd.er_entities import Entity, Relation, XMLObject

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

    def iter_relations(self, filter_):
        for relation in self.relations:
            if filter_(relation):
                yield relation
            elif len(relation) == 2 and filter_(relation.invert()):
                yield relation.invert()


ERD.__repr__ = make_repr('entities', 'relations')
