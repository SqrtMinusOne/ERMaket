# from typing import List

# from api.erd.er_entities import Entity, Relation
# from api.erd.rd_entities import Column, Table

from .factory import Factory

__all__ = ['Algorithm']


class Algorithm:
    def __init__(self, erd):
        self.erd = erd

        self._entities_to_tables = {}
        self._tables = {}

    def run_algorithm(self):
        self._make_tables()
        self._merge_tables()
        self._set_auto_pks()

    def _get_table(self, entity_id):
        return self._tables[self._entities_to_tables[entity_id]]

    def _make_tables(self):
        """Make tables from entities"""
        for entity in self.erd.entities.values():
            assert entity.name not in self._tables
            table = Factory.entity_to_table(entity, auto_pk=False)
            self._tables[table.name] = table
            self._entities_to_tables[entity._id] = table.name

    def _merge_tables(self):
        """Merge tables where possible (1:1 mandatory relationships)"""
        for relation in self.erd.relations:
            if all([
                    side.is_mandatory and not side.is_multiple
                    for side in relation.sides
            ]):
                table = self.entities_to_tables[relation.sides[0].id_ref]
                for side in relation.sides[1:]:
                    ignore_pk = table.pk is not None
                    columns = self._get_table(side.id_ref).columns
                    Factory.add_columns(table, columns, ignore_pk=ignore_pk)
                    self._entities_to_tables[side.id_ref] = table.name

    def _set_auto_pks(self):
        """Add auto ids where required"""
        for table in self._tables.values():
            if table.pk is None:
                Factory.auto_pk(table)
