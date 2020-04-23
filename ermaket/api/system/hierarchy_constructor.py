import logging

import stringcase

from ermaket.api.models import NamesConverter as Names
from ermaket.api.system.hierarchy import (
    AccessRight, AccessRights, DisplayColumn, Hierachy, LinkedTableColumn,
    RoleAccess, Section, Table, TableColumn, TableLinkType
)

from .system_tables_hierarchy import make_system_tables_hierarchy

__all__ = ['HierachyConstructor']

SYSTEM_SECTION = 'System'


class HierachyConstructor:
    def __init__(self, tables, schema, admin_role=None):
        self._tables = tables
        self._schema = schema
        self._admin_role = admin_role

    def construct(self):
        h = Hierachy()
        parent = Section(
            accessRights=self._global_rights(),
            name=stringcase.sentencecase(self._schema)
        )
        h.append(parent)
        for table in self._tables.values():
            t = self._make_table(table)
            h.append(t)
            parent.children.append(t.id)
        h.set_tree()
        return h

    def insert_system_pages(self, h):
        parent = h.get_by_name(SYSTEM_SECTION)
        if parent:
            logging.info('Section with system pages already exists')
            return
        make_system_tables_hierarchy(self._admin_role.name, h)
        h.set_tree()

    def _global_rights(self):
        rights = AccessRights(inherit=False)
        if self._admin_role:
            rights.append(
                RoleAccess(
                    self._admin_role.name,
                    [AccessRight.VIEW, AccessRight.CHANGE, AccessRight.DELETE]
                )
            )
        return rights

    def _make_table(self, table):
        t = Table(
            accessRights=AccessRights(),
            name=stringcase.sentencecase(table.name),
            tableName=table.name,
            schema=self._schema
        )
        for column in table.columns:
            t.columns.append(self._make_column(column))

        local_fks = set([fk_col.name for fk_col in table.foreign_keys])

        for relation in table.relationships:
            if relation.fk_col and relation.fk_col.name in local_fks:
                t.columns.append(self._make_linked_fk_column(relation))
                if relation.fk_col.pk:
                    t.columns.append(self._make_hidden_pk_column(relation))
                else:
                    display_column = relation.display_column
                    if display_column is not None:
                        t.displayColumns.append(
                            DisplayColumn(
                                rowName=self._linked_name(relation),
                                linkRowName=display_column.name,
                                isMultiple=False
                            )
                        )
            else:
                t.columns.append(self._make_linked_nofk_column(relation))
                display_column = relation.display_column
                if display_column is not None:
                    t.displayColumns.append(
                        DisplayColumn(
                            rowName=self._linked_name(relation),
                            linkRowName=display_column.name,
                            isMultiple=relation.other_side.is_multiple
                        )
                    )

        t.formDescription = t.make_form()
        t.set_default_sort()
        if t.empty:
            t.hidden = True

        return t

    def _linked_name(self, relation):
        if relation.secondary_table is not None:
            return Names.referrer_rel_name(
                relation.ref_table.name, relation.name
            )
        elif relation.fk_col is not None:
            return Names.referrer_rel_name(
                relation.ref_table.name, relation.name
            )
        else:
            return Names.referral_rel_name(
                relation.ref_table.name, relation.name
            )

    def _make_linked_fk_column(self, relation):
        return LinkedTableColumn(
            self._linked_name(relation),
            linkTableName=relation.ref_table.name,
            linkSchema=self._schema,
            fkName=relation.fk_col.name,
            type=relation.fk_col.type_,
            isRequired=relation.other_side.is_mandatory,
            isMultiple=False,
            linkRequired=relation.this_side.is_mandatory,
            linkMultiple=relation.this_side.is_multiple,
            linkName=relation.name,
            linkType=TableLinkType(TableLinkType.DROPDOWN),
            isUnique=relation.fk_col in relation.table.uniques
        )

    def _make_linked_nofk_column(self, relation):
        return LinkedTableColumn(
            self._linked_name(relation),
            linkTableName=relation.ref_table.name,
            linkSchema=self._schema,
            isMultiple=relation.other_side.is_multiple,
            linkRequired=relation.this_side.is_mandatory,
            linkMultiple=relation.this_side.is_multiple,
            linkName=relation.name,
            linkType=TableLinkType(TableLinkType.COMBINED),
            isRequired=relation.other_side.is_mandatory,
            isUnique=False,
            isFilter=False,
            isSort=False
        )

    def _make_hidden_pk_column(self, relation):
        col = self._make_column(relation.fk_col)
        col.isVisible = False
        return col

    def _make_column(self, column):
        params = dict(
            rowName=column.name,
            isPk=column.pk,
            isRequired=column.not_null,
            type=column.type_,
            isUnique=column.unique,
            isAuto=column.auto_inc,
            isEditable=not column.auto_inc
        )
        if (column.type_ == 'timestamp'):
            params['dateFormat'] = 'DD-MM-YYYY HH:mm:ss'
        elif (column.type_ == 'time'):
            params['dateFormat'] = 'HH:mm:ss'
        elif (column.type_ == 'date'):
            params['dateFormat'] = 'DD-MM-YYYY'
        return TableColumn(**params)
