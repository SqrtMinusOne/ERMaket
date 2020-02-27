from typing import Dict, List

from bs4 import BeautifulSoup
from magic_repr import make_repr

from api import Config
from api.erd.er_entities import Entity, Relation
from utils.xml import XMLObject

__all__ = ['ERD']


class ERD:
    def __init__(self, xml=None):
        self._config = Config()
        if xml is not None:
            self.soup = BeautifulSoup(xml, 'xml')
        else:
            self.soup = BeautifulSoup(features='xml')
            self.soup.append(
                self.soup.new_tag(
                    'erModel', **self._config.XML['ErRootAttributes']
                )
            )
        XMLObject.soup = self.soup

        self.entities: Dict[int, Entity] = {}
        self.relations: List[Relation] = []

        self._parse_xml()

    def add_entity(self, entity: Entity):
        assert entity._id not in self.entities
        self.entities[entity._id] = entity

    def add_relation(self, relation: Relation):
        self.relations.append(relation)

    def _parse_xml(self):
        for tag in self.soup.find_all('entity'):
            entity = Entity.from_xml(tag)
            self.add_entity(entity)

        self.relations = [
            Relation.from_xml(tag) for tag in self.soup.find_all('relation')
        ]

    def iter_relations(self, filter_):
        for relation in self.relations:
            if filter_(relation):
                yield relation
            elif len(relation) == 2 and filter_(relation.invert()):
                yield relation.invert()

    def to_xml(self):
        soup = BeautifulSoup(features='xml')
        soup.append(
            soup.new_tag('erModel', **self._config.XML['ErRootAttributes'])
        )
        root = soup.find('erModel')
        XMLObject.soup = self.soup
        for entity in self.entities.values():
            root.append(entity.to_xml())
        for relation in self.relations:
            root.append(relation.to_xml())
        return soup


ERD.__repr__ = make_repr('entities', 'relations')
