from ermaket.api.system.hierarchy import (
    AccessRight, AccessRights, Button, Buttons, Hierachy, LinkedTableColumn,
    Location, PrebuiltPage, PrebuiltPageType, RoleAccess, Section,
    SystemAction, Table, TableColumn, TableLinkType
)

__all__ = ['make_system_tables_hierarchy']

NAMES = {
    'parentSection': 'System tables',
    'userTable': {
        'name': 'Users',
        'login': 'Login',
        'roles': 'Roles',
    },
    'rolesTable':
        {
            'name': 'Roles',
            'role_name': 'Name',
            'is_default': 'Default',
            'can_reset_password': 'Reset passwords',
            'has_sql_access': 'SQL Access',
            'can_register_all': 'Register all',
            'can_register': 'Register roles',
            'users': 'Users',
        },
    'tokenTable':
        {
            'name': 'Tokens',
            'token_name': 'Name',
            'infinite': 'Unlimited uses',
            'uses': 'Remaining uses',
            'time_limit': 'Time limit',
            'description': 'Description'
        }
}


def make_system_tables_hierarchy(admin_role, h=None):
    if h is None:
        h = Hierachy()
    parent = _parent_section(admin_role)
    h.append(parent)
    sql = _sql()
    user = _user_table()
    role = _roles_table()
    token = _token_table()

    h.append(sql)
    h.append(user)
    h.append(role)
    h.append(token)
    parent.children.append(sql.id)
    parent.children.append(user.id)
    parent.children.append(role.id)
    parent.children.append(token.id)


def _parent_section(admin_role):
    rights = AccessRights(inherit=False)
    rights.append(
        RoleAccess(
            admin_role,
            [AccessRight.VIEW, AccessRight.CHANGE, AccessRight.DELETE]
        )
    )
    return Section(accessRights=rights, name=NAMES['parentSection'])


def _sql():
    sql = PrebuiltPage(
        accessRights=AccessRights(),
        name='SQL Console',
        type=PrebuiltPageType.SQL
    )
    return sql


def _user_table():
    t = Table(
        accessRights=AccessRights(),
        name=NAMES['userTable']['name'],
        tableName='user',
        schema='system'
    )
    t.columns.append(
        TableColumn(
            name=NAMES['userTable']['login'],
            rowName='login',
            isPk=True,
            isRequired=True,
            isUnique=True,
            type='varchar(256)',
            isEditable=False
        )
    )
    t.columns.append(
        LinkedTableColumn(
            name=NAMES['userTable']['roles'],
            rowName='roles',
            linkTableName='role',
            linkSchema='system',
            isMultiple=True,
            isRequired=False,
            linkRequired=False,
            linkMultiple=True,
            linkType=TableLinkType(TableLinkType.COMBINED),
            isUnique=False,
        )
    )
    t.buttonList = Buttons(
        [
            Button(
                text='Make registration token',
                location=Location.CARDHEADER,
                variant='outline-light',
                icon='["fas", "key"]',
                action=SystemAction.REGTOKEN,
            ),
            Button(
                location=Location.ACTION,
                icon='["fas", "unlock"]',
                action=SystemAction.PASSTOKEN,
                tooltip="Reset password"
            )
        ]
    )
    return t


def _roles_table():
    t = Table(
        accessRights=AccessRights(),
        name=NAMES['rolesTable']['name'],
        tableName='role',
        schema='system'
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['role_name'],
            rowName='name',
            isPk=True,
            isRequired=True,
            isUnique=True,
            type='varchar(256)',
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['is_default'],
            rowName='is_default',
            isRequired=True,
            type='boolean',
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['can_reset_password'],
            rowName='can_reset_password',
            isRequired=True,
            type='boolean',
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['has_sql_access'],
            rowName='has_sql_access',
            isRequired=True,
            type='boolean',
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['can_register_all'],
            rowName='can_register_all',
            isRequired=True,
            type='boolean',
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['rolesTable']['can_register'],
            rowName='can_register',
            type='array',
        )
    )
    t.columns.append(
        LinkedTableColumn(
            name=NAMES['rolesTable']['users'],
            rowName='users',
            linkTableName='user',
            linkSchema='system',
            isMultiple=True,
            isRequired=False,
            linkRequired=False,
            linkMultiple=True,
            linkType=TableLinkType(TableLinkType.COMBINED),
            isUnique=False,
        )
    )
    return t


def _token_table():
    t = Table(
        accessRights=AccessRights(),
        name=NAMES['tokenTable']['name'],
        tableName='token',
        schema='system'
    )
    t.columns.append(
        TableColumn(
            name=NAMES['tokenTable']['token_name'],
            rowName='name',
            type='varchar(256)'
        )
    )
    t.columns.append(
        TableColumn(
            rowName='token_hash',
            type='varchar(256)',
            isPk=True,
            isRequired=True,
            isEditable=False,
            isUnique=True,
            isVisible=False,
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['tokenTable']['infinite'],
            rowName='infinite',
            isRequired=True,
            type='boolean'
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['tokenTable']['uses'],
            rowName='uses',
            isRequired=True,
            type='int4'
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['tokenTable']['time_limit'],
            rowName='time_limit',
            type='time_limit'
        )
    )
    t.columns.append(
        TableColumn(
            name=NAMES['tokenTable']['description'],
            rowName='description',
            isRequired=True,
            type='json'
        )
    )
    return t
