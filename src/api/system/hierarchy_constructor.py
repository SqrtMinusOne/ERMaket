from api.system.hierarchy import (AccessRight, AccessRights, Hierachy,
                                  RoleAccess, Section, Table, TableColumn,
                                  LinkedTableColumn)


class HierachyConstructor:
    def __init__(self, tables, schema, admin_role=None):
        self._tables = tables
        self._schema = schema
        self._admin_role = admin_role

    def construct(self):
        h = Hierachy()
        parent = Section(
            accessRights=self._global_rights(),
            name=self._schema,
            id=h._next_id()
        )
        h.append(parent)
        for table in self._tables.values():
            t = self._make_table(table)
            t.id = h._next_id()
            h.append(t)
            parent.children.append(t.id)
        return h

    def _global_rights(self):
        rights = AccessRights()
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
            t.columns.append(TableColumn(column.name))

        for relation in table.relationships:
            t.columns.append(LinkedTableColumn(relation.name))

        t.form = t.make_form()

        return t
