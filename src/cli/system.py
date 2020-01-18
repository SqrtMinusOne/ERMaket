import click

from api.system import SystemManager, UserManager

__all__ = ['system']


@click.group(help='System management')
def system():
    pass


@system.command(help='Add user')
@click.option("--login", prompt=True)
@click.option(
    "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
@click.option("--role", multiple=True)
def useradd(login, password):
    UserManager().add_user(login, password)


@system.command(help='Create system tables (drop via db drop)')
def create():
    SystemManager().create_system_tables()
