import logging
from typing import Dict

from magic_repr import make_repr

from api.erd.er_entities import Entity
from api.erd.rd_entities import Column, ForeignKey, Table
from api.models import NamesConverter

from .factory import Factory

__all__ = ['Algorithm']

default_options = {
    "joint_unique_index": True,
    "respect_n_obligation": False,
    "nullable_1n_fk": False
}


class Algorithm:
    def __init__(self, erd, options={}):
        self.erd = erd
        self.options = {**default_options, **options}

        self._entities_to_tables: Dict[int, Entity] = {}
        self._tables: Dict[str, Table] = {}

    def run_algorithm(self):
        self._make_tables()
        self._merge_tables()
        self._inject_system_refs()

        self._make_one_table()
        self._make_with_secondary()

        self._set_pks()
        self._resolve_fks()
        self._resolve_check_not_last()
        self._apply_fixes()

        logging.info(
            f'Converted {len(self.erd.entities)} entities'
            f' and {len(self.erd.relations)}'
            f' relations to {len(self._tables)} tables'
        )

    @property
    def tables(self):
        return self._tables

    def _get_table(self, entity_id):
        return self._tables[self._entities_to_tables[entity_id]]

    def _make_tables(self):
        """Make tables from entities"""
        for entity in self.erd.entities.values():
            assert entity.name not in self._tables
            table = Factory.entity_to_table(entity, auto_pk=False)
            self._tables[table.name] = table
            self._entities_to_tables[entity._id] = table.name

    def _merge_tables(self):  # OK
        """Merge tables where possible (1:1 mandatory relationships)"""
        relations = self.erd.iter_relations(
            lambda relation: all(
                [
                    side.is_mandatory and not side.is_multiple
                    for side in relation.sides
                ]
            )
        )
        for relation in relations:
            table = self._get_table(relation.sides[0].id_ref)
            for side in relation.sides[1:]:
                ignore_pk = table.pk is not None
                columns = self._get_table(side.id_ref).columns
                Factory.add_columns(table, columns, ignore_pk=ignore_pk)
                del self._tables[self._entities_to_tables[side.id_ref]]
                self._entities_to_tables[side.id_ref] = table.name

    def _inject_system_refs(self):
        """
        Inject references to system tables

        """
        for entity in self.erd.entities.values():
            if entity.system_table is not None:
                table = self._tables[self._entities_to_tables[entity._id]]
                table._system_ref = entity.system_table

    def _make_one_table(self):
        """
        1(mandatory)     - 1(non-mandatory)
        1(mandatory)     - n(mandatory)
        1(mandatory)     - n(non-mandatory)
        1(not-mandatory) - n(mandatory) & nullable_1n_fk
        """
        def filter_condition(relation):
            return (
                len(relation) == 2 and (
                    (
                        relation.sides[0].is_mandatory and
                        not relation.sides[0].is_multiple and (
                            relation.sides[1].is_multiple or (
                                not relation.sides[1].is_mandatory and
                                not relation.sides[1].is_multiple
                            )
                        )
                    ) or (
                        not relation.sides[0].is_mandatory and
                        not relation.sides[0].is_multiple and
                        relation.sides[1].is_multiple and
                        relation.sides[1].is_mandatory and
                        self.options['nullable_1n_fk']
                    )
                )
            )

        for relation in self.erd.iter_relations(filter_condition):
            table1 = self._get_table(relation.sides[0].id_ref)  # 1
            table2 = self._get_table(relation.sides[1].id_ref)  # n or 1(n)
            Factory.direct_link(
                relation, table1, table2, self.options['respect_n_obligation']
            )

    def _make_with_secondary(self):
        """
        1(non-mandatory) - 1(non-mandatory)
        1(not-mandatory) - n(mandatory) & not nullable_1n_fk
        1(non-mandatory) - n(non-mandatory)
        n(any) - n(any)
        non-binary
        """
        def filter_condition(relation):
            return (
                (
                    len(relation) == 2 and (
                        (
                            (
                                not relation.sides[0].is_mandatory and
                                not relation.sides[0].is_multiple and
                                not relation.sides[1].is_mandatory
                            ) or (
                                not relation.sides[0].is_mandatory and
                                not relation.sides[0].is_multiple and
                                relation.sides[1].is_multiple and
                                relation.sides[1].is_mandatory and
                                not self.options['nullable_1n_fk']
                            )
                        ) or (
                            relation.sides[0].is_multiple and
                            relation.sides[1].is_multiple
                        )
                    )
                ) or (len(relation) > 3)
            )

        for relation in self.erd.iter_relations(filter_condition):
            tables = [self._get_table(side.id_ref) for side in relation.sides]
            new_table = Factory.secondary_link(
                relation, tables, self.options['respect_n_obligation'],
                self.options['joint_unique_index']
            )
            self._tables[new_table.name] = new_table

    def _set_pks(self):
        unresolved = (t for t in self.tables.values() if t.pk is None)
        for table in unresolved:
            if not self._try_fk_as_pk(table):
                Factory.auto_pk(table)

    def _try_fk_as_pk(self, table):
        if len(table.columns) == 0 and len(table.foreign_keys) > 0:
            for fk_col in table.foreign_keys:
                fk_col.pk = True
            return True
        for fk in table.foreign_keys:
            if fk.unique:
                fk.pk = True
                return True
        return False

    def _resolve_fks(self):
        for table in self.tables.values():
            for fk_col in table.foreign_keys:
                self._set_fk_column(fk_col.fk)
                fk_col.resolve_type()
                fk_col.name = NamesConverter.fk_name(
                    fk_col.fk.table.name, fk_col.fk.column.name
                )

    def _set_fk_column(self, fk):
        if fk.column is None:
            assert (
                isinstance(fk.table.pk, Column) or
                isinstance(fk.table.pk, ForeignKey)
            )
            fk.column = fk.table.pk

    def _resolve_check_not_last(self):
        for table in self.tables.values():
            for relationship in table.check_not_empty:
                counterpart = relationship.ref_rel
                relationship.ref_table.check_not_last.append(counterpart)

    def _apply_fixes(self):
        for table in self._tables.values():
            table.remove_duplicate_names()
            table.resolve_recursive_relationships()


Algorithm.__repr__ = make_repr('_tables')
