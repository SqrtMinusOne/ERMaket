import stringcase

from api.models import NamesConverter as Names
from api.system.hierarchy import (AccessRight, AccessRights, Hierachy,
                                  LinkedTableColumn, RoleAccess, Section,
                                  Table, TableColumn, TableLinkType)


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

        for relation in table.relationships:
            if relation.fk_col:
                t.columns.append(
                    self._make_linked_fk_column(relation)
                )
            else:
                t.columns.append(
                    self._make_linked_nofk_column(relation)
                )

        t.formDescription = t.make_form()
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
            isUnique=False
        )

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
