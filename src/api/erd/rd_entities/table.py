from typing import List, Union

from magic_repr import make_repr

from .column import Column
from .relationship import ORMRelationship

__all__ = ['Table']


class Table:
    def __init__(self, name, columns: List[Column]):
        self.name = name
        self.columns = columns
        self.foreign_keys: List[Column] = []
        self.relationships: List[ORMRelationship] = []

    def add_fk(self, fk: Column):
        self.foreign_keys.append(fk)

    def add_rel(self, rel: ORMRelationship):
        self.relationships.append(rel)

    @property
    def primary_rels(self):
        return filter(lambda rel: rel.secondary_table is None,
                      self.relationships)

    @property
    def secondary_rels(self):
        return filter(lambda rel: rel.secondary_table is not None,
                      self.relationships)

    @property
    def pk(self) -> Union[Column, List[Column]]:
        pks = [
            column for column in self.columns + self.foreign_keys if column.pk
        ]
        if len(pks) == 0:
            return None
        if len(pks) == 1:
            return pks[0]
        return pks


Table.__repr__ = make_repr('name', 'columns', 'foreign_keys', 'relationships')
