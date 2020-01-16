from api.system.hierarchy import (AccessRight, AccessRights, Hierachy,
                                  RoleAccess, Section, Table)


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
            id=h.next_id()
        )
        h.sections.append(parent)

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
            accessRights=AccessRights(), name=table.name, tableName=table.name
        )
