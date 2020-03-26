import click

from api.system import UserManager

__all__ = ['system']


@click.group(help='System management')
def system():
    pass


@system.command(help='Add role')
@click.option('--name', prompt=True)
@click.option(
    '--default', is_flag=True, help='Add the role as default for new users'
)
@click.option('--reset-pass', is_flag=True, help='Can reset passwords')
@click.option('--sql', is_flag=True, help='SQL Access')
@click.option('--link-schema', help='Linked schema name', default=None)
@click.option('--link-entity', help='Linked entity id', default=None)
def roleadd(name, default, reset_pass, sql, link_schema, link_entity):
    UserManager().add_role(
        name=name,
        is_default=default,
        can_reset_password=reset_pass,
        has_sql_access=sql,
        linked_entity_schema=link_schema,
        linked_entity_id=link_entity,
    )


@system.command(help='Add user')
@click.option("--login", prompt=True)
@click.option(
    "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
@click.option("--role", multiple=True)
def useradd(login, password, role):
    UserManager().add_user(login, password, role_names=role)
