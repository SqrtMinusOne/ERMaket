from typing import Dict

from magic_repr import make_repr

from api.erd.er_entities import Entity
from api.erd.rd_entities import Column, ForeignKey, Table

from .error import ModelError
from .factory import Factory

__all__ = ['Algorithm']

default_options = {"1x_to_nn_as_3": False}


class Algorithm:
    def __init__(self, erd, options={}):
        self.erd = erd
        self.options = {**default_options, **options}

        self._entities_to_tables: Dict[int, Entity] = {}
        self._tables: Dict[str, Table] = {}

    def run_algorithm(self):
        self._make_tables()
        self._merge_tables()
        self._make_1m_to_1n()
        self._make_1x_to_nm()
        self._make_1n_to_1n()
        self._make_1x_to_nn()
        self._make_nx_to_nx()
        self._make_non_binary()

        self._set_pks()
        self._resolve_fks()

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

    def _merge_tables(self):
        """Merge tables where possible (1:1 mandatory relationships)"""
        relations = self.erd.iter_relations(lambda relation: all([
            side.is_mandatory and not side.is_multiple
            for side in relation.sides
        ]))
        for relation in relations:
            table = self._get_table(relation.sides[0].id_ref)
            for side in relation.sides[1:]:
                ignore_pk = table.pk is not None
                columns = self._get_table(side.id_ref).columns
                Factory.add_columns(table, columns, ignore_pk=ignore_pk)
                del self._tables[self._entities_to_tables[side.id_ref]]
                self._entities_to_tables[side.id_ref] = table.name

    def _make_1m_to_1n(self):
        """1(mandatory):(1:non-mandatory)"""
        def filter_condition(relation):
            return (len(relation) == 2 and not relation.sides[0].is_multiple
                    and not relation.sides[1].is_multiple
                    and relation.sides[0].is_mandatory
                    and not relation.sides[1].is_mandatory)

        for relation in self.erd.iter_relations(filter_condition):
            table1 = self._get_table(relation.sides[0].id_ref)  # mandatory
            table2 = self._get_table(relation.sides[1].id_ref)  # non-mandatory
            self._link_tables(table1, table2, relation.name, unique=True)

    def _make_1x_to_nm(self):
        """1(any):n(mandatory)"""
        def filter_condition(relation):
            return (len(relation) == 2 and relation.sides[0].is_multiple
                    and not relation.sides[1].is_multiple
                    and relation.sides[0].is_mandatory)

        for relation in self.erd.iter_relations(filter_condition):
            table1 = self._get_table(relation.sides[0].id_ref)  # n
            table2 = self._get_table(relation.sides[1].id_ref)  # 1
            self._link_tables(table2, table1, relation.name, unique=False)

    def _link_tables(self, table1, table2, name, unique=True, recursive=True):
        """Add fk to table2

        :param table1:
        :param table2:
        :param recurvise:
        """
        if not recursive and table1 == table2:
            raise ModelError(f'Tables {table1}, {table2} cannot have relation'
                             'because they are one table')
        table2.add_fk(ForeignKey(table1, name=name, unique=unique))

    def _make_1n_to_1n(self):
        """1:1 non-mandatory"""
        def filter_condition(relation):
            return (len(relation) == 2 and all([
                not side.is_mandatory and not side.is_multiple
                for side in relation.sides
            ]))

        for relation in self.erd.iter_relations(filter_condition):
            self._make_link_table(relation)

    def _make_1x_to_nn(self):
        """1 (any): n(non-mandatory)"""
        def filter_condition(relation):
            return (len(relation) == 2 and relation.sides[0].is_multiple
                    and not relation.sides[1].is_multiple
                    and not relation.sides[0].is_mandatory)

        for relation in self.erd.iter_relations(filter_condition):
            if self.options['1x_to_nn_as_3']:
                self._make_link_table(relation)
            else:
                table1 = self._get_table(relation.sides[0].id_ref)  # n
                table2 = self._get_table(relation.sides[1].id_ref)  # 1
                self._link_tables(table2, table1, relation.name, unique=False)

    def _make_nx_to_nx(self):
        def filter_condition(relation):
            return (len(relation) == 2 and relation.sides[0].is_multiple
                    and relation.sides[1].is_multiple)

        for relation in self.erd.iter_relations(filter_condition):
            self._make_link_table(relation)

    def _make_non_binary(self):
        def filter_condition(relation):
            return len(relation) > 2

        for relation in self.erd.iter_relations(filter_condition):
            self._make_link_table(relation)

    def _make_link_table(self, relation):
        tables = [self._get_table(side.id_ref) for side in relation.sides]
        new_table = Factory.relation_to_table(relation, tables)
        self._tables[new_table.name] = new_table

    def _set_pks(self):
        unresolved = (t for t in self.tables.values() if t.pk is None)
        for table in unresolved:
            if not self._try_fk_as_pk(table):
                Factory.auto_pk(table)

    def _try_fk_as_pk(self, table):
        if len(table.columns) == 0 and len(table.foreign_keys) > 0:
            for fk in table.foreign_keys:
                fk.pk = True
            return True
        for fk in table.foreign_keys:
            if fk.unique:
                fk.pk = True
                return True
        return False

    def _resolve_fks(self):
        for table in self.tables.values():
            for fk in table.foreign_keys:
                self._set_fk_column(fk)

    def _set_fk_column(self, fk):
        if fk.column is None:
            assert (isinstance(fk.table.pk, Column)
                    or isinstance(fk.table.pk, ForeignKey))
            fk.column = fk.table.pk


Algorithm.__repr__ = make_repr('_tables')
