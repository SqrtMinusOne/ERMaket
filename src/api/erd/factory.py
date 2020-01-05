from typing import List

from api.erd.er_entities import Attribute, Entity
from api.erd.rd_entities import Column, Table


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
        table = Table(name=entity.name, columns=columns)
        if auto_pk:
            Factory.auto_pk(table)
        return table

    @staticmethod
    def auto_pk(table):
        if not any([column.pk for column in table.columns]):
            table.columns = [Factory._auto_id(), *table.columns]

    @staticmethod
    def add_attributes(table: Table,
                       attributes: List[Attribute],
                       ignore_pk=False):
        """Add attributes to existing table

        :param table:
        :type table: Table
        :param attributes:
        :type attributes: List[Attribute]
        :param ignore_pk: Whether to ignore primary keys for attributes
        """
        columns = [
            Factory._attribute_to_column(attr, ignore_pk)
            for attr in attributes
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
        column = Column(name=attribute.name, type_=attribute.type_)
        if attribute.is_pk and not ignore_pk:
            column.pk = True
        return column

    @staticmethod
    def _auto_id():
        """A column with autonumerating integer"""
        return Column(name='id', type_='int8', auto_inc=True, pk=True)
