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
        self.check_not_empty: List[ORMRelationship] = []
        self.check_not_last: List[ORMRelationship] = []
        self.uniques: List[Column] = []
        self._system_ref = None

    def add_fk(self, fk: Column):
        self.foreign_keys.append(fk)

    def add_rel(self, rel: ORMRelationship, add_check=False):
        self.relationships.append(rel)
        if add_check:
            self.check_not_empty.append(rel)

    def remove_duplicate_names(self):
        used_names = {}
        repeats = {}
        for col in [*self.columns, *self.foreign_keys]:
            if col.name not in used_names:
                used_names[col.name] = col
            else:
                if col.name in repeats:
                    repeats[col.name].append(col)
                else:
                    repeats[col.name] = [used_names[col.name], col]
        for name, cols in repeats.items():
            for i, col in enumerate(cols):
                col.name = f"{col.name}_{i}"

    def resolve_recursive_relationships(self):
        recursive = [
            rel for rel in self.relationships if rel.table == rel.ref_table
        ]
        resolved = set()
        for rel in recursive:
            if rel.name in resolved:
                self.relationships.remove(rel)
                continue
            if rel.secondary_table:
                fk = next(
                    col for col in rel.secondary_table.foreign_keys
                    if col.fk.relation_name == rel.name
                )
                rel.fk_col = fk
            resolved.add(rel.name)

    @property
    def primary_rels(self):
        return filter(
            lambda rel: rel.secondary_table is None, self.relationships
        )

    @property
    def secondary_rels(self):
        return filter(
            lambda rel: rel.secondary_table is not None, self.relationships
        )

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
