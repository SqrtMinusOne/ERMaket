from itertools import permutations, combinations
from typing import List

from api.erd.er_entities import Attribute, Entity, Relation
from api.erd.rd_entities import Column, ForeignKey, ORMRelationship, Table
from api.models import NamesConverter

__all__ = ['Factory']


class Factory:
    """A class for converting ER entities to RD"""
    @staticmethod
    def entity_to_table(entity: Entity, auto_pk=True) -> Table:
        """Convert an entity with attributes to a table with columns.


        :param entity:
        :type entity: Entity
        :param auto_pk: If no pk's are found, add autonumerating integer id
        column
        :rtype: Table
        """
        columns = [
            Factory._attribute_to_column(attr) for attr in entity.attributes
        ]
        table = Table(
            name=NamesConverter.table_name(entity.name), columns=columns
        )
        if auto_pk:
            Factory.auto_pk(table)
        return table

    @staticmethod
    def make_fk(
        table,
        *args,
        ondelete='cascade',
        onupdate='cascade',
        relation_name=None,
        **kwargs
    ):
        return Column(
            fk=ForeignKey(
                table,
                ondelete=ondelete,
                onupdate=onupdate,
                relation_name=relation_name,
            ),
            *args,
            **kwargs
        )

    def make_rel(table, add_check=False, *args, **kwargs):
        rel = ORMRelationship(table=table, *args, **kwargs)
        table.add_rel(rel, add_check=add_check)
        return rel

    @staticmethod
    def direct_link(relation: Relation, table1: Table, table2: Table, resp_n):
        a, b = relation.sides[0], relation.sides[1]
        fk_col = Factory.make_fk(
            table1,
            relation_name=relation.name,
            unique=not b.is_multiple,
            not_null=not a.is_mandatory,
            onupdate='cascade',
            ondelete='cascade'
        )
        table2.add_fk(fk_col)  # add fk to b

        ref_rel = Factory.make_rel(  # add rel to b
            table2,
            ref_table=table1,
            name=relation.name,
            fk_col=fk_col,
            relation=relation,
            side_index=1
        )
        Factory.make_rel(  # add rel to a
            table1,
            ref_table=table2,
            ref_rel=ref_rel,
            name=relation.name,
            relation=relation,
            side_index=0,
            add_check=resp_n and b.is_mandatory
        )

    def secondary_link(
        relation: Relation, tables: List[Table], add_check: bool, junique: bool
    ):
        if len(tables) == 2:
            name = f"{tables[0].name}_{relation.name}_{tables[1].name}"
        else:
            name = relation.name
        name = NamesConverter.table_name(name)
        linked = Table(name=name, columns=[])
        fks = [
            Factory.make_fk(
                table,
                relation_name=relation.name,
                unique=False,
                not_null=False,
                onupdate='cascade',
                ondelete='cascade'
            ) for table in tables
        ]
        [linked.add_fk(fk) for fk in fks]
        unique = [
            i for i in range(len(relation.sides))
            if not relation.sides[i].is_multiple
        ]
        if len(unique) == 1 or len(unique) > 1 and junique:
            linked.uniques = [fks[i] for i in unique]

        rels = [
            Factory.make_rel(
                tables[i1],
                add_check=add_check and relation.sides[i2].is_mandatory,
                ref_table=tables[i2],
                name=relation.name,
                secondary_table=linked,
                relation=relation,
                side_index=i1
            ) for i1, i2 in permutations(range(len(tables)), 2)
        ]
        [
            setattr(r1, 'ref_rel', r2)
            for r1, r2 in combinations(rels, 2)
        ]
        return linked

    @staticmethod
    def auto_pk(table):
        if not any([column.pk for column in table.columns]):
            table.columns = [Factory._auto_id(), *table.columns]

    @staticmethod
    def fk_as_pk(table, fk):
        col = Column(fk.column.name, fk.column.type_, pk=True)
        fk.self_column = col

    @staticmethod
    def add_attributes(
        table: Table, attributes: List[Attribute], ignore_pk=False
    ):
        """Add attributes to existing table

        :param table:
        :type table: Table
        :param attributes:
        :type attributes: List[Attribute]
        :param ignore_pk: Whether to ignore primary keys for attributes
        """
        columns = [
            Factory._attribute_to_column(a, ignore_pk) for a in attributes
        ]
        table.columns.extend(columns)

    @staticmethod
    def add_columns(table: Table, columns: List[Column], ignore_pk=False):
        if ignore_pk:
            for column in columns:
                column.pk = False
        table.columns.extend(columns)

    @staticmethod
    def _attribute_to_column(attribute: Attribute, ignore_pk=False) -> Column:
        """Convert an attribute to a column

        :param attribute:
        :type attribute: Attribute
        :param ignore_pk: Whether to ignore primary key
        :rtype: Column
        """
        name = NamesConverter.attribute_name(attribute.name)
        column = Column(name=name, type_=attribute.type_)
        if attribute.is_pk and not ignore_pk:
            column.pk = True
        return column

    @staticmethod
    def _auto_id():
        """A column with autonumerating integer"""
        return Column(name='id', type_='int8', auto_inc=True, pk=True)
