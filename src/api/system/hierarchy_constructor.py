from api.system.hierarchy import (AccessRight, AccessRights, Hierachy,
                                  LinkedTableColumn, RoleAccess, Section,
                                  Table, TableColumn)


class HierachyConstructor:
    def __init__(self, tables, schema, admin_role=None):
        self._tables = tables
        self._schema = schema
        self._admin_role = admin_role

    def construct(self):
        h = Hierachy()
        parent = Section(accessRights=self._global_rights(), name=self._schema)
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
            accessRights=AccessRights(), name=table.name, schema=self._schema
        )
        for column in table.columns:
            t.columns.append(
                TableColumn(
                    column.name, isPk=column.pk, isRequired=column.not_null
                )
            )

        for relation in table.relationships:
            if (relation.fk_col):
                t.columns.append(
                    LinkedTableColumn(
                        relation.name,
                        linkTableName=relation.ref_table.name,
                        linkSchema=self._schema,
                        fkName=relation.fk_col.name,
                        isMultiple=False,
                        isRequired=relation.fk_col.not_null
                    )
                )
            else:
                t.columns.append(
                    LinkedTableColumn(
                        relation.name,
                        linkTableName=relation.ref_table.name,
                        linkSchema=self._schema,
                        isMultiple=relation.is_multiple,
                        isRequired=False  # TODO
                    )
                )

        t.formDescription = t.make_form()
        return t
