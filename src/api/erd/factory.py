from itertools import permutations
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
        add_rel=True,
        **kwargs
    ):
        return Column(
            fk=ForeignKey(
                table,
                ondelete=ondelete,
                onupdate=onupdate,
                relation_name=relation_name,
                add_rel=add_rel
            ),
            *args,
            **kwargs
        )

    @staticmethod
    def make_rel(table, fk_col):
        fk = fk_col.fk
        assert fk.add_rel is True
        table.add_rel(
            ORMRelationship(
                table=table,
                ref_table=fk.table,
                name=fk.relation_name,
                fk_col=fk_col
            )
        )
        fk.table.add_rel(
            ORMRelationship(
                table=fk.table, ref_table=table, name=fk.relation_name
            )
        )

    @staticmethod
    def relation_to_table(relation: Relation, tables: List[Table]) -> Table:
        if len(tables) == 2:
            name = f"{tables[0].name}_{relation.name}_{tables[1].name}"
        else:
            name = relation.name
        name = NamesConverter.table_name(name)
        table = Table(name=name, columns=[])
        [
            table.add_fk(
                Factory.make_fk(
                    linked, relation_name=relation.name, add_rel=False
                )
            ) for linked in tables
        ]
        [
            table1.add_rel(
                ORMRelationship(
                    table=table1,
                    ref_table=table2,
                    name=relation.name,
                    secondary_table=table
                )
            ) for table1, table2 in permutations(tables, 2)
        ]
        return table

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
